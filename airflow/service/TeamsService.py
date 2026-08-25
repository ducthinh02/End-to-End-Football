from .DatabaseConnection import DatabaseConnection
from extract.team import TeamExtractor
from loads.TeamsLoader import TeamLoader
import logging

logger = logging.getLogger(__name__)

class TeamsService(DatabaseConnection):    
    
    def __init__(self, extractor: TeamExtractor):
        super().__init__()
        self.extractor = extractor
        
    def run(self):
        competitions = ["WC","ELC","CL","PL","EC","FL1","BL1","SA","PD"]
        
        loader = TeamLoader(self.conn)
        try:
            for competition in competitions:
                
                try:
                    teams = self.extractor.extract_teams_by_competition(competition)

                    if not teams:
                        logger.warning(
                            f"No match data found for competition: {competition}")
                        continue
                    
                    loader.load_team(teams)
                    loader.load_team_competition(teams)
                    self.conn.commit()
                    logger.info(
                        "Team pipeline completed successfully."
                    )
                
                except Exception as e:
                    if self.conn:
                        self.conn.rollback()
                    logger.error(f"Teams pipeline failed for {competition}. Error: {str(e)}")
                    
            
        finally:    
            self.close()
            
        
    