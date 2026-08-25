from extract.competitions import CompetitionsExtractor
from loads.CompetitionsLoader import CompetitionLoader
from .DatabaseConnection import DatabaseConnection
import logging

logger = logging.getLogger(__name__)

class CompetitionService(DatabaseConnection):
    
    def __init__(self,
                extractor: CompetitionsExtractor):
        
        super().__init__()
        
        self.extractor = extractor
        
    
    def run(self):

        
        try:
            competition = self.extractor.extract_competition()
            if not competition:
                raise ValueError("No competition data found")
            
            loader = CompetitionLoader(self.conn)
            loader.load_competition(
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
            self.close
