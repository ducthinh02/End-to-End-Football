from psycopg2.extensions import connection
 
import logging

logger = logging.getLogger(__name__)

class AreaLoad():
    
    def __init__(self, conn:connection):
        
        self.conn = conn
    
    def load_area(self, 
                  areas: dict):

        if not areas:
            raise ValueError("Không tìm thấy dữ liệu!")
        
        logger.info(
        "Loading area: %s",
        areas)

        rows = []
        areas:list = areas.get("areas")
        for area in areas:
            row = (
                area.get("id"),
                area.get("name"),
                area.get("countryCode"),
                area.get("parentAreaId"),
                area.get("parentArea")
                    
            )
            rows.append(row)
        
        sql = """
            INSERT INTO raw.areas (
                area_id ,

                area_name ,
                area_code , 

                parent_area_id ,
                parent_area_name
            )
                VALUES(
                    %s,%s,%s,%s,%s
                )
                ON CONFLICT(area_id)
                
                DO UPDATE SET

                    area_name  = EXCLUDED.area_name,
                    area_code  = EXCLUDED.area_code, 

                    parent_area_id  = EXCLUDED.parent_area_id,
                    parent_area_name = EXCLUDED.parent_area_name
                """
        
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows
                )
                logger.info(
                    "Loaded %s areas",
                    len(rows)
                )
        
        except Exception:
            
            logger.exception(
                "Failed load area"
            )
            raise
             

        