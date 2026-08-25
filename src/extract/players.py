from .BaseExtractor import BaseExtractor
import logging

logger = logging.getLogger(__name__)

class PlayerExtractor(BaseExtractor):
    
    def extract_player(
            self,person_id:int)->dict:

        logger.info(
            "Extract player: %s",
            person_id
        )

        player_data = self.client.get_player(person_id)

        if not player_data:
            raise ValueError(
                f"Không tìm thấy dữ liệu của player {person_id}"
                )
        
        logger.info(
            "Đã lấy dữ liệu thành công: %s",
            person_id
        )

        return player_data


    def extract_topScorers(
            self,competitions_code:str)->dict:

        logger.info(
            "Extract player: %s",
            competitions_code
        )

        topScorers_data = self.client.get_topScorers(competitions_code)

        if not topScorers_data:
            raise ValueError(
                f"Không tìm thấy dữ liệu của player {competitions_code}"
                )
        
        logger.info(
            "Đã lấy dữ liệu thành công: %s",
            competitions_code
        )

        return topScorers_data
    