from psycopg2.extensions import connection
import logging

logger = logging.getLogger(__name__)

class TeamLoader:
    def __init__(self, conn: connection):
        super().__init__(),
        self.conn = conn
    
    def load_team(self,teams: dict):
        
        if not teams:
            raise ValueError("Data not found")

        logger.info(
            "Loading teams: %s",
            teams
            )
        
        rows = []
    
        # season = teams.get("season",{}).get("id")
        
        for team in teams.get("teams",[]):
            row = (
                team.get("id"),
                team.get("name"),
                team.get("shortName"),
                team.get("tla"),
                team.get("crest"),
                team.get("area",{}).get("id"),
                team.get("address"),
                team.get("website"),
                team.get("founded"),
                team.get("venue"),
                # team.get("runningCompetitions",{}).get("id"),
                # team.get("runningCompetitions",{}).get("code"),
                # team.get("coach",{}).get("id"),
                # team.get("coach",{}).get("name"),
                # team.get("marketValue"),
                team.get("lastUpdated")
                
            )
            
            rows.append(row)
        
        sql = """
            INSERT INTO raw.teams (
                team_id, 

                team_name,
                team_short_name,
                team_tla,

                team_crest,

                area_id,

                team_address ,
                team_website ,

                team_founded ,
                team_venue ,
                
                api_last_updates  
            )   VALUES(
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s
            )
            
            ON CONFLICT("team_id")
            DO UPDATE SET
                team_name = EXCLUDED.team_name,
                team_short_name= EXCLUDED.team_short_name,
                team_tla= EXCLUDED.team_tla,

                team_crest= EXCLUDED.team_crest,

                area_id= EXCLUDED.area_id,

                team_address = EXCLUDED.team_address,
                team_website = EXCLUDED.team_website,

                team_founded = EXCLUDED.team_founded,
                team_venue = EXCLUDED.team_venue,

                
                api_last_updates = EXCLUDED.api_last_updates
        """
        try:
           
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows
                )
           
            logger.info(
                "Loaded %s teams",
                len(rows))
        except:
            logger.exception(
                "failed to load teams"
            )
            raise 
    
    
    def load_team_competition(self,teams: dict):
        
        if not teams:
            raise ValueError("Data not found")
    
        logger.info(
            "Loading teams: %s",
            teams
                )    
        
        rows = []
        
        competition = teams.get("competition",{}).get("id")
        season = teams.get("season",{}).get("id")
        
        for team in teams.get("teams",[]):
            row = (
                                
                team.get("id"),
            
                competition,
                season,
                team.get("coach",{}).get("id"),
                team.get("coach",{}).get("name")
            )
            rows.append(row)
        
        sql = """
            INSERT INTO raw.team_competition(
                team_id ,

                competition_id ,
                
                season_id,
                
                coach_id    ,
                coach_name  
            )
            VALUES(
                %s,%s,%s,
                %s,%s
            )ON CONFLICT(
                        team_id,
                        competition_id
                        )
            DO UPDATE SET
                coach_id = EXCLUDED.coach_id,
                coach_name = EXCLUDED.coach_name
        """
        
        try:
            
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows
                    )
                
            logger.info(
                "Loaded %s teams",
                len(rows)
                )
            
        except:
            logger.exception(
                "failed to load teams"
                )
            raise 