from psycopg2.extensions import connection

import logging

logger = logging.getLogger(__name__)

class MatchesLoader:
    
    
    def __init__(self, conn: connection):
        super().__init__()
        self.conn = conn
    
    
    def load_match(self, matches:dict):
        
        if not matches:
            raise ValueError(
                "Match data not found"
                )
            
        logger.info(
            "Loading matches: %s",
            matches
            )
        
        rows = []
        
        for match in matches.get("matches") or []:
            comp = match.get("competition") or {}
            season = match.get("season") or {}
            home_team = match.get("homeTeam") or {}
            away_team = match.get("awayTeam") or {}
            score = match.get("score") or {}
            full_time = score.get("fullTime") or {}
            half_time = score.get("halfTime") or {}
            regularTime = score.get("regularTime") or {}
            extraTime = score.get("extraTime") or {}
            penalties = score.get("penalties") or {}
            row = (
                match.get("id"),
                comp.get("id"),
                season.get("id"),
                match.get("utcDate"),
                match.get("status"),
                match.get("matchday"),
                match.get("stage"),
                home_team.get("id"),
                away_team.get("id"),
                score.get("winner"),
                score.get("duration"),
                full_time.get("home"),
                full_time.get("away"),
                half_time.get("home"),
                half_time.get("away"),
                
                regularTime.get("home"),
                regularTime.get("away"),
                
                extraTime.get("home"),
                extraTime.get("away"),
                                
                penalties.get("home"),
                penalties.get("away"),
                
                match.get("lastUpdated")
            )
            rows.append(row)
        
        sql = """
            INSERT INTO raw.matches(
                match_id      ,
        
                competition_id  ,
                season_id,

                utcDate         ,
                match_status    ,
                match_day       ,
                stage           ,

                home_team_id    ,
                away_team_id    ,

                winner          ,
                duration        ,

                fullTime_home   ,
                fullTime_away   ,

                halfTime_home   ,
                halfTime_away   ,

                regularTime_home ,
                regularTime_away ,

                extraTime_home  ,
                extraTime_away ,

                penalties_home  ,
                penalties_away  ,

                api_last_update
            )   VALUES(
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s
            )   ON CONFLICT (match_id)
                DO UPDATE SET
                    competition_id = EXCLUDED.competition_id,
                    season_id = EXCLUDED.season_id,
                    utcDate = EXCLUDED.utcDate,
                    match_status = EXCLUDED.match_status,
                    match_day = EXCLUDED.match_day,
                    stage = EXCLUDED.stage,
                    home_team_id = EXCLUDED.home_team_id,
                    away_team_id = EXCLUDED.away_team_id,
                    winner = EXCLUDED.winner,
                    duration = EXCLUDED.duration,
                    fullTime_home = EXCLUDED.fullTime_home,
                    fullTime_away = EXCLUDED.fullTime_away,
                    halfTime_home = EXCLUDED.halfTime_home,
                    halfTime_away = EXCLUDED.halfTime_away,
                    
                    regularTime_home = EXCLUDED.regularTime_home,
                    regularTime_away = EXCLUDED.regularTime_away,
                    
                    extraTime_home = EXCLUDED.extraTime_home,
                    extraTime_away = EXCLUDED.extraTime_away,
                    
                    penalties_home = EXCLUDED.penalties_home,
                    penalties_away = EXCLUDED.penalties_away,
                    
                    api_last_update = EXCLUDED.api_last_update
            """
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(
                    sql,
                    rows
                )
            
            logger.info(
                "Loaded %s competitions.",
                len(rows)
                )
        except Exception:
            logger.exception(
                "failed to load competitions"
            )
            raise
        
        
        