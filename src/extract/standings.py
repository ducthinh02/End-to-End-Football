from .BaseExtractor import BaseExtractor
import logging

logger = logging.getLogger(__name__)

class StandingsExtractor(BaseExtractor):

    def extract_standing_for_competition(
            self, competitions_code:str,season_year:int)-> dict:
        
        logger.info(
            "Extract competition: %s",
            competitions_code
        )
        standingFC_data = self.client.get_standing(competitions_code,season_year)

        if not standingFC_data:
            raise ValueError(
                "Không tìm thấy dữ liệu bảng xếp hạng ở giải đấu: ",
                competitions_code

                )
        
        logger.info(
            "Đã lấy dữ liệu bảng xếp hạng thành công:%s",
            standingFC_data["standings"]
        )
        return standingFC_data
