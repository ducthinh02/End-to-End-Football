from extract.players import PlayerExtractor
from loads.TSLoader import TSLoader
from .DatabaseConnection import DatabaseConnection
import logging

logger = logging.getLogger(__name__)

class TopSoccerService(DatabaseConnection):
    
    def __init__(self,
                extractor: PlayerExtractor):
        
        super().__init__()
        
        self.extractor = extractor
        
    
    def run(self):

        competitions = ["WC","ELC","CL","PL","EC","FL1","BL1","SA","PD"]
        loader = TSLoader(self.conn)
        try:
            
            for competition_code in competitions:
                                
                if not competition_code:
                    raise ValueError(f"No competition data found: {competition_code}")
                
                topSoccer = self.extractor.extract_topScorers(competition_code)
                
                loader.load_topSoccer(
                    topSoccer
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
