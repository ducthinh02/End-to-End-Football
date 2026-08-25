from .DatabaseConnection import DatabaseConnection

from loads.AreasLoad import AreaLoad
from extract.areas import AreasExtractor
import logging


logger = logging.getLogger(__name__)

class AreaService(DatabaseConnection):
    def __init__(self, 
                extractor:AreasExtractor):
        
        super().__init__()
        self.extractor = extractor
        
    def run(self):
        
        try:
            area = self.extractor.extract_area()
            if not area:
                raise ValueError("No area data found") 

            loader = AreaLoad(self.conn)
            
            loader.load_area(area)
            
            self.conn.commit()
            
            logger.info(
                "Area pipeline completed successfully!"   
            )      
        
        except Exception:
            self.conn.rollback()
            
            logger.info(
                "Area pipeline failed."
            )
            raise
        finally:
            self.close