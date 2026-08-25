from psycopg2.extensions import connection

import logging

logger = logging.getLogger(__name__)

class SeasonsLoader:

    def __init__(self, conn:connection):

        self.conn = conn
        
    def load_seasons(self,
                competitions: dict):

        logger.info(
        "Loading competitions: %s",
        competitions)

        if not competitions :
            raise ValueError("Không tìm thấy dữ liệu!")
        
        rows = []
        seasons:list[dict] = competitions.get("seasons")
        competition_id = competitions.get("id")
        for season in seasons:
            winner = season.get("winner") or {}
            row = (
                season.get("id"),
                competition_id,
                season.get("startDate"),
                season.get("endDate"),
                season.get("currentMatchday"),
                winner.get("id"),
                season.get("stages"),
            )
            rows.append(row)
    
        sql = """
            INSERT INTO raw.season (
                
                season_id      ,
                competition_id ,
                start_date     ,
                end_date       ,
                currentMatchday ,
                winner_team_id ,
                stages    
      
                ) 
                
                VALUES(
                %s,%s,%s,%s,
                %s,%s,%s
                )
                ON CONFLICT(competition_id,season_id)
                
                DO UPDATE SET
                    start_date = EXCLUDED.start_date ,
                    end_date = EXCLUDED.end_date ,
                    currentMatchday = EXCLUDED.currentMatchday,
                    winner_team_id = EXCLUDED.winner_team_id,
                    stages = EXCLUDED.stages

            """
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows)
                    
            logger.info(
                "Loaded %s competitions.",
                len(rows)
                )
        except Exception:
            logger.exception(
                "failed to load competitions"
            )
            raise