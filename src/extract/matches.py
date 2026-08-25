from .BaseExtractor import BaseExtractor
import logging

logger = logging.getLogger(__name__)

class MatchesExtractor(BaseExtractor):
    
    def extract_matches_for_competitions(self,
                 competitions_code: str)->dict:

        logger.info(
            "Extract Matches for competition: %s",
            competitions_code
        )

        matchesFC_data = self.client.get_competition_matches(competitions_code)

        if not matchesFC_data:
            raise ValueError(
                f"Không tìm thấy dữ liệu trận đấu: {competitions_code}"
            )
        
        logger.info(
            "Đã lấy dữ liệu thành công trận đấu: %s",
            competitions_code
        )
        return matchesFC_data
    

    def extract_matches(self, match_id:int)->dict:
        
        logger.info(
            "Extract Matches for competition: %s",
            match_id
        )

        matches_data = self.client.get_matches(match_id)

        if not matches_data:
            raise ValueError(
                f"Không tìm thấy dữ liệu trận đấu: {match_id}"
            )
        
        logger.info(
            "Đã lấy dữ liệu thành công trận đấu: %s",
            match_id
        )
        return matches_data