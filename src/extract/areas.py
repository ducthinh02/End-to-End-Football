from .BaseExtractor import BaseExtractor
import logging

logger = logging.getLogger(__name__)


class AreasExtractor(BaseExtractor):

    def extract_area(self)-> dict:

        logger.info(
            "Extract area: %s", 
            )
        
        area = self.client.get_area()

        if not area:
            raise ValueError (
                f"Không tìm thấy dữ liệu area"
            )
        
        logger.info(
            "Đã lấy dữ liệu area %s thành công ",
            area.get("name")
            )
 
        return area
    
        