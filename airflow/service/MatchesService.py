from .DatabaseConnection import DatabaseConnection
from extract.matches import MatchesExtractor
from loads.MatchesLoader import MatchesLoader 
import logging

logger = logging.getLogger(__name__)

class MatchesService(DatabaseConnection):    
    
    def __init__(self, extractor: MatchesExtractor):
        super().__init__()
        self.extractor = extractor
        
    def run(self):
        competitions = ["WC","ELC","CL","PL","EC","FL1","BL1","SA","PD"]
        
        loader = MatchesLoader(self.conn)
        try:
            for competition in competitions:
                
                logger.info(f"Starting matches extraction for {competition}...")
                
                try:
                    matches = self.extractor.extract_matches_for_competitions(competition)
                    
                    if not matches:
                        logger.warning(f"No match data found for competition: {competition}")
                        continue
                    
                
                    loader.load_match(matches)
                    self.conn.commit()
                    logger.info(
                        "Matches pipeline completed successfully."
                    )
                
                except Exception as e:
                    if self.conn:
                        self.conn.rollback()
                    logger.error(
                        f"Matches pipeline failed for {competition}. Error: {str(e)}"
                        )
                    
            
        finally:    
            self.close()
            logger.info("Database connection closed for MatchesService.")
        
    