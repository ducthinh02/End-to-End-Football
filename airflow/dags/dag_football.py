import pendulum
from airflow.decorators import dag,task
from src.extract.competitions import CompetitionsExtractor
from src.storage.minio_client import MinIOClient
from datetime import datetime
from src.extract.standings import StandingsExtractor
from src.extract.matches import MatchesExtractor
from src.extract.team import TeamExtractor
from src.loads.CompetitionsLoader import CompetitionLoader
from src.loads.StandingsLoader import StandingsLoader
from src.loads.MatchesLoader import MatchesLoader
from src.loads.SeasonsLoader import SeasonsLoader
from src.loads.TeamsLoader import TeamLoader
from src.storage.postgres_client import PostgresClient
from datetime import timedelta
from src.extract.areas import AreasExtractor
from src.loads.AreasLoad import AreaLoad

from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
import time
import logging

logger = logging.getLogger(__name__)
LIST_COMPETITIONS = ["WC","ELC","CL","PL","EC","FL1","BL1","SA","PD"]
season_year = [2018,2019,2020,2021,2022,2023]

default_args={
    "owner": "data_team",
    "retries":3,
    "retry_delay":timedelta(seconds=10)}
    


@dag(
    dag_id= "football_pipeline",
    schedule= "@daily",
    start_date= pendulum.datetime(2026,8,20, tz="Asia/Ho_Chi_Minh"),
    end_date= pendulum.datetime(2026,8,24, tz="Asia/Ho_Chi_Minh"),
    default_args=default_args,
    catchup= False,
    max_active_runs=1,       
    tags=["elt","competition"],
) 
def football_pipeline():
    
    @task
    def extract_competition(competition_code: str, ds:str=None)-> str:
        competitions = CompetitionsExtractor()
        
        minio = MinIOClient()        
                        
        datas_competition : dict = competitions.extract_competition_for_code(
                                    competition_code=competition_code)
            
        if not datas_competition:
            raise ValueError("Not found data")    
                    
        object_key = (
                f"raw/competition/"
                f"{competition_code}/"
                f"date={ds}/"
                f"data.json"
            )        
            

        minio.upload_json(data=datas_competition, object_name=object_key)
        time.sleep(1)
            
        return object_key
    @task
    def extract_area(ds:str=None)-> str:
            areas = AreasExtractor()
            
            minio = MinIOClient()        
                            
            datas_areas : dict = areas.extract_area()
                
            if not datas_areas:
                raise ValueError("Not found data")    
                        
            object_key = (
                    f"raw/Areas/"
                    f"date={ds}/"
                    f"data.json"
                )        
                
    
            minio.upload_json(data=datas_areas, object_name=object_key)
            
            time.sleep(1)
                
            return object_key
        
    @task
    def extract_teams(competition_code: str, ds: str=None)-> str:

        minio = MinIOClient()

        datas_teams= TeamExtractor()
        
        try:
                data_json: dict = datas_teams.extract_teams_by_competition(
                    competitions_code=competition_code)
            
        except Exception as e:
                logger.error("Failed: %s - %s: %s",
                            competition_code,
                            e)
                raise
            
        object_key = (
                f"raw/teams/"
                f"competition_code={competition_code}/"
                f"date={ds}/"
                f"data.json"
            )
        minio.upload_json(data= data_json,object_name=object_key)    
        time.sleep(1)    
        return object_key

    
    @task()
    def extract_standings(competition_code: str, ds: str=None):        

        minio = MinIOClient()


        object_keys= []
        datas_standing= StandingsExtractor()
                        
        for year in season_year:            
                try:        
                    data_json:dict = datas_standing.extract_standing_for_competition(
                        competitions_code=competition_code,season_year=year)
                except Exception as e: 
                    logger.error("Failed: %s - %s: %s",
                        competition_code,
                        year,
                        e
                        )
                    raise
                
                if not data_json:
                    logger.warning(
                        "No standings data: %s - %s",
                        competition_code,
                        year
                    )
                    continue
                                                            
                object_key = (
                    f"raw/standings/"
                    f"competition_code={competition_code}/"
                    f"season_year={year}/"
                    f"date={ds}/"
                    f"data.json"
                )
                
                minio.upload_json(data=data_json,object_name=object_key)
                object_keys.append(object_key)
                time.sleep(1)

        return object_keys
    
    @ task
    def extract_matches(competition_code: str, ds: str = None)-> str:                

        minio = MinIOClient()
        
        datas_matches= MatchesExtractor()                
                                
        data_json:dict = datas_matches.extract_matches_for_competitions(competitions_code=competition_code)
                        
        if not data_json:
                raise ValueError("Not found data")
                                
                        
        object_key = (
                f"raw/matches/"
                f"{competition_code}/"
                f"date={ds}/"
                f"data.json"
                )
                        
        minio.upload_json(data=data_json,object_name=object_key)
        time.sleep(1)
        
        return object_key
    

    @task
    def load_competitions(object_keys):
        
        minio = MinIOClient()
        connection = PostgresClient()
        
        competitions_loader = CompetitionLoader(connection)
        
        try:
            for object_key in object_keys:
                try:
                    competitions = minio.download_json(object_name=object_key)
                    
                    if not competitions:
                        logger.warning("No data found for object_key=%s",
                        object_key)
                        continue
                    
                    competitions_loader.load_competition(competitions=competitions)
                    connection.conn.commit()
                    
                except Exception as e:
                    if connection.conn:
                        connection.conn.rollback()
                        logger.error(f"Competition pipeline failed for {object_key}. Error: {str(e)}")
                    raise
        
        finally:
            if connection.conn:
                connection.conn.close()
    
    @task
    def load_areas(object_keys):
            
            minio = MinIOClient()
            connection = PostgresClient()
            
            areas_loader = AreaLoad(connection)
            
            try:
                    try:
                        areas_data = minio.download_json(object_name=object_keys)
                        
                        if not areas_data:
                            logger.warning("No data found for object_key=%s",
                            object_keys)
                            
                        
                        areas_loader.load_area(areas_data)
                        connection.conn.commit()
                        
                    except Exception as e:
                        if connection.conn:
                            connection.conn.rollback()
                            logger.error(f"Areas pipeline failed for {object_keys}. Error: {str(e)}")
                        raise
            
            finally:
                if connection.conn:
                    connection.conn.close()
    
    
    @task
    def load_standings(object_keys: list[list[str]]):
        minio = MinIOClient()
        connection = PostgresClient()
        
        flat_keys = [key for object_key in object_keys for key in object_key]
            
        
        standings_loader = StandingsLoader(connection)
        
        try:    
            for key in flat_keys:
                try:
                
                    standings = minio.download_json(object_name=key)
                
                    if not standings:
                        logger.warning("No data found for object_key=%s",
                            key)
                        continue
                
                    standings_loader.load_standings(standings=standings)
                    connection.conn.commit()
                
                except Exception as e:
                    if connection.conn:
                        connection.conn.rollback()
                        logger.error(f"Standings pipeline failed for {key}. Error: {str(e)}")
                    
                    raise
        finally:
            if connection.conn:

                connection.conn.close()
                
    @task            
    def load_matches(object_keys):

        minio = MinIOClient()
        connection = PostgresClient()
            
        matches_loader = MatchesLoader(connection)
        try:
            for object_key in object_keys:
                try:
                    matches = minio.download_json(object_name=object_key)
                    
                    if not matches:
                        logger.warning("No data found for object_key=%s",
                        object_key)
                        continue
                    
                    matches_loader.load_match(matches=matches)        

                    connection.conn.commit()
                    
                except Exception as e:
                    if connection.conn:
                        connection.conn.rollback()
                        logger.error(f"Matches pipeline failed for {object_key}. Error: {str(e)}")
                    raise
        
        finally:
            if connection.conn:
                connection.conn.close()                
                
    @task
    def load_teams(object_keys):
        
        minio = MinIOClient()
        connection = PostgresClient()       
        
        team_loader = TeamLoader(connection)
        try:            
            for object_key in object_keys:
                try:
                    teams = minio.download_json(object_name=object_key)
                                
                    if not teams:
                        logger.warning("No data found for object_key=%s",
                        object_key)
                        continue
                                
                    team_loader.load_team(teams=teams)
                    team_loader.load_team_competition(teams=teams)
                    
                    connection.conn.commit()
                
                except Exception as e:
                    if connection.conn:
                        connection.conn.rollback()
                        logger.error(f"teams pipeline failed for {object_key}. Error: {str(e)}")
                    raise
        
        finally:
            if connection.conn:
                connection.conn.close()
                
    @task
    def load_season(object_keys):
        minio = MinIOClient()
        connection = PostgresClient()
        season_loader= SeasonsLoader(conn=connection)
        
        try:
            for object_key in object_keys:
                try:
                    season = minio.download_json(object_name=object_key)
                    
                    if not season:
                        logger.warning("No data found for object_key=%s",
                        object_key)
                        continue
                    
                    season_loader.load_seasons(season)
                    
                    connection.conn.commit()
            
                except Exception as e:
                    if connection.conn:
                        connection.conn.rollback()
                        logger.error(f"Season pipeline failed for {object_key}. Error: {str(e)}")
                        raise
        finally:
            if connection.conn:
                connection.conn.close()
    
    trigger_dbt_dag= TriggerDagRunOperator(
        task_id="trigger_dbt_transformation",
        trigger_dag_id="dbt_transform_pipeline",
        wait_for_completion=False
    )
    
    competition_keys = extract_competition.expand(competition_code= LIST_COMPETITIONS)
    areas_keys = extract_area()
    matches_keys= extract_matches.expand(competition_code= LIST_COMPETITIONS)
    standings_keys= extract_standings.expand(competition_code= LIST_COMPETITIONS)
    teams_keys= extract_teams.expand(competition_code= LIST_COMPETITIONS)
    
    task_load_comps= load_competitions(competition_keys)
    task_load_areas= load_areas(areas_keys)
    task_load_team= load_teams(teams_keys)
    
    
    task_load_standings= load_standings(standings_keys)
    task_load_matches= load_matches(matches_keys)
    task_load_season = load_season(competition_keys)
    
    task_load_areas>>task_load_comps
    task_load_comps>>task_load_season
    
    [task_load_comps,task_load_areas]>>task_load_team
    [task_load_comps,task_load_team,task_load_season]>>task_load_standings
    [task_load_comps,task_load_team,task_load_season]>>task_load_matches
    
    [task_load_standings,task_load_matches,task_load_season]>>trigger_dbt_dag
    
football_pipeline()