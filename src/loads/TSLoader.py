from psycopg2.extensions import connection
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class TSLoader:
    
    def __init__(self, conn: connection):
        super().__init__()
        self.conn = conn
    
    def load_topSoccer(
            self,
            topSoccer: dict):
        
        if not topSoccer:
            raise ValueError("Data for top soccer of the season not found")
        
        logger.info(
            "Loading top Soccer: %s",
            topSoccer
        )
        
        competition_id = topSoccer.get("competition",{}).get("id")
        season_id = topSoccer.get("season",{}).get("id")
        
        api_last_update = datetime.now(
            timezone.utc
        )
        
        rows = []
        
        for soccer in topSoccer.get("scorers",[]):
            row = (
                competition_id,
                season_id,
                
                soccer.get("player",{}).get("id"),
                soccer.get("team",{}).get("id"),
                soccer.get("goals"),
                soccer.get("assists"),
                soccer.get("penalties"),
                api_last_update
            )
            rows.append(row)
        
        sql = """
            INSERT INTO raw.Top_scorers (
                competition_id ,
                season_id      ,
                player_id      , 
                team_id        ,

                goals          ,
                assists        ,
                penalties      ,
                
                api_last_update
            )   
            VALUES (
                %s,%s,%s,%s,
                %s,%s,%s,%s
            )
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows
                )
            
            logger.info(
                            "Loaded %s Top Soccers.",
                            len(rows)
                            )
            
        except Exception:
            
            logger.exception(
                            "failed to load Top Soccers."
                        )
            raise

        
        
    