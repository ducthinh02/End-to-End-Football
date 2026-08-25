import logging
from .BaseExtractor import BaseExtractor

logger = logging.getLogger(__name__)


class CompetitionsExtractor(BaseExtractor):
    
    def extract_competition_for_code(self,competition_code)->dict : 
            
            logger.info(
                "Extract competition: %s",
                )
            
            competition_data = self.client.get_competition_for_code(competition_code)
            
            if not competition_data:
                raise ValueError(
                    f"Competition not found, {competition_code}"
                    )
            
            logger.info(
                "Đã lấy dữ liệu giải đấu thành công %s,}",
                competition_data.get("name")
            )
            
            return competition_data
    
    
    
    
    def extract_competition(self)->dict : 
        
        logger.info(
            "Extract competition: %s",
            )
        
        competition_data = self.client.get_competition()
        
        if not competition_data:
            raise ValueError(
                f"Competition not found"
                )
        
        logger.info(
            "Đã lấy dữ liệu giải đấu thành công %s",
            competition_data.get("name")
        )
        
        return competition_data
