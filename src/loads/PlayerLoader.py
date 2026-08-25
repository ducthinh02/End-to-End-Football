from psycopg2.extensions import connection
import logging

logger = logging.getLogger(__name__)

class PlayerLoader:
    
    def __init__(self, conn:connection):
        
        self.conn = conn
    
    def load_player(self, players: dict):
        
        if not players:
            raise ValueError("Data not found")
        
        logger.info(
                "Load player: %s ",
                players
            )
        
        
        rows = []
        
        
        row = (
            players.get("id"),
            players.get("name"),
            players.get("firstName"),
            players.get("lastName"),
            players.get("dateOfBirth"),
            players.get("nationality"),
            players.get("position"),
            players.get("shirtNumber"),
            players.get("lastUpdated")    
            )
        rows.append(row)
        
        sql = """
            INSERT INTO raw.player (
                player_id  ,

                player_name     ,
                player_firstName ,
                player_lastName  ,

                date_of_birth   ,
                nationality     ,

                position    ,
                shirt_number ,
                
                api_last_update
            )
            VALUES(
                %s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            ON CONFLICT(player_id)
            DO UPDATE SET
                player_name = EXCLUDED.player_name ,
                player_firstName = EXCLUDED.player_firstName,
                player_lastName = EXCLUDED.player_lastName,

                date_of_birth = EXCLUDED.date_of_birth,
                nationality = EXCLUDED.nationality,

                position = EXCLUDED.position,
                shirt_number = EXCLUDED.shirt_number,
                
                api_last_update = EXCLUDED.api_last_update
        
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows
                )
        
        except Exception:
            logger.exception(
                "failed to load player"
            )
            raise 
                
        