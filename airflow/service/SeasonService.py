from extract.competitions import CompetitionsExtractor
from loads.SeasonsLoader import SeasonsLoader
from .DatabaseConnection import DatabaseConnection
import logging

logger = logging.getLogger(__name__)

class SeasonService(DatabaseConnection):
    
    def __init__(self,
                extractor: CompetitionsExtractor):
        
        super().__init__()
        
        self.extractor = extractor
        
    
    def run(self):

        competitions = ["WC","ELC","CL","PL","EC","FL1","BL1","SA","PD"]
        loader = SeasonsLoader(self.conn)
        try:
            
            for competition_code in competitions:
                
                competition = self.extractor.extract_competition_for_code(competition_code)
                
                if not competition:
                    raise ValueError(f"No competition data found: {competition_code}")
                
                
                loader.load_seasons(
                    competition
                )
                
                self.conn.commit()
                
                logger.info(
                    "Competition pipeline completed successfully."
                )

        except Exception:
            self.conn.rollback()

            logger.info(
                "Competition pipeline failed."
            )
            raise
        finally:
            self.close()
