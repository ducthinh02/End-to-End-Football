from psycopg2.extensions import connection

import logging

logger = logging.getLogger(__name__)

class CompetitionLoader:

    def __init__(self, conn:connection):

        self.conn = conn
        
    def load_competition(self,
                competitions: dict):

        logger.info(
        "Loading competitions: %s",
        competitions)

        if not competitions :
            raise ValueError("Không tìm thấy dữ liệu!")
        
        rows = []
        row = (
                competitions.get("id"),
                competitions.get("area", {}).get("id"),
                competitions.get("name"),
                competitions.get("code"),
                competitions.get("type"),
                competitions.get("emblem"),
                competitions.get("currentSeason", {}).get("id"),
                competitions.get("numberOfAvailableSeasons"),
                competitions.get("lastUpdated"),
            )
        rows.append(row)
    
        sql = """
            INSERT INTO raw.competition (
                competition_id,
                area_id,
                competition_name,
                competition_code,

                competition_type,
                competition_emblem,
    
                current_season_id,
                number_of_available_seasons,
    
                api_last_update
      
                ) 
                
                VALUES(
                %s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                ON CONFLICT(competition_id)
                
                DO UPDATE SET
                    area_id = EXCLUDED.area_id,

                    competition_name = EXCLUDED.competition_name,
                    competition_code = EXCLUDED.competition_code,

                    competition_type = EXCLUDED.competition_type,
                    competition_emblem = EXCLUDED.competition_emblem,
    
                    current_season_id = EXCLUDED.current_season_id,
                    number_of_available_seasons = EXCLUDED.number_of_available_seasons,
    
                    api_last_update = EXCLUDED.api_last_update

            """
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(sql,
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