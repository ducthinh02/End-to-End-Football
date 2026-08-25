from .DatabaseConnection import DatabaseConnection
from extract.standings import StandingsExtractor
from loads.StandingsLoader import StandingsLoader
import logging

logger = logging.getLogger(__name__)

class StandingsService(DatabaseConnection):    
    
    def __init__(self, extractor: StandingsExtractor):
        super().__init__()
        self.extractor = extractor
        
    def run(self):
        competitions = ["WC","ELC","CL","PL","EC","FL1","BL1","SA","PD"]
        
        loader = StandingsLoader(self.conn)
        try:
            for competition in competitions:
                
                logger.info(f"Starting standings extraction for {competition}...")
                
                try:
                    standings = self.extractor.extract_standing_for_competition(competition)
                    
                    if not standings:
                        logger.warning(f"No standing data found for competition: {competition}")
                        continue
                    
                
                    loader.load_standings(standings)
                    self.conn.commit()
                    logger.info(
                        "Standings pipeline completed successfully."
                    )
                
                except Exception as e:
                    self.conn.rollback()
                    logger.error(
                        f"Standings pipeline failed for {competition}. Error: {str(e)}"
                        )
                    
            
        finally:    
            self.close()
            logger.info("Database connection closed for StandingsService.")
        
    