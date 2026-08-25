from psycopg2.extensions import connection

import logging

logger = logging.getLogger(__name__)

class StandingsLoader:
    
    
    def __init__(self, conn: connection):
        super().__init__()
        self.conn = conn
    
    
    def load_standings(self, standings:dict):
        
        if not standings:
            raise ValueError(
                "Standings data not found"
                )
            
        logger.info(
            "Loading standings: %s",
            standings
            )
        
        rows = []
        season:dict = standings.get("season",{}).get("id") 
        competition:dict = standings.get("competition",{}).get("id")
        standing_list = standings.get("standings",[])           
        
        for standing in standing_list:
            
            tables:list[dict]= standing.get("table") or []
            stage = standing.get("stage")
            standing_type = standing.get("type")         
            for table in tables:
                    
                    
                row = (
                        
                    season,
                    competition,

                    stage,
                    standing_type,
                    
                    table.get("position"),
                    table.get("team",{}).get("id"),
                    table.get("playedGames"),
                    table.get("won"),
                    table.get("draw"),
                    table.get("lost"),
                    table.get("points"),
                    table.get("goalsFor"),
                    table.get("goalsAgainst"),
                    table.get("goalDifference"),   
                                    
                    )
                rows.append(row)
        
        sql = """
            INSERT INTO raw.standing(
                season_id ,
                competition_id  ,

                stage           ,
                standing_type   ,

                position    ,
                team_id        ,
                
                playedGames     ,

                won             ,
                draw            ,
                lost            ,

                points          ,

                goalsfor        ,
                goalsAgainst    ,
                goalDifference  
            ) VALUES(
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s
            )ON CONFLICT (
                competition_id,
                season_id,
                team_id,
                stage,
                standing_type
            )
            DO UPDATE SET
                position = EXCLUDED.position,
                playedGames = EXCLUDED.playedGames,
                won = EXCLUDED.won,
                draw = EXCLUDED.draw,
                lost = EXCLUDED.lost,
                points = EXCLUDED.points,
                goalsfor = EXCLUDED.goalsfor,
                goalsAgainst = EXCLUDED.goalsAgainst,
                goalDifference = EXCLUDED.goalDifference;
            """
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows
                )
            
            logger.info(
                "Loaded %s STANDINGS.",
                len(rows)
                )
        except Exception:
            logger.exception(
                "failed to load STANDINGS"
            )
            raise
        
        
        