from .BaseExtractor import BaseExtractor
import logging


logger = logging.getLogger(__name__)


class TeamExtractor(BaseExtractor):

    def extract_teams_by_competition(
            self, competitions_code: str)-> dict:

        logger.info("Extract team: %s", competitions_code)
        
        teams_for_competition = self.client.get_team_ForCompetitions(competitions_code)

        if not teams_for_competition:
            raise ValueError(f"Không tìm thấy dữ liệu của các đội bóng ở giải {competitions_code}")
        
        logger.info(
            "Đã lấy dữ liệu đội bóng thành công: %s",
            teams_for_competition.get("count")
        )

        return teams_for_competition 
    
    def extract_team(self,teamId):

        logger.info("Extract team: %s", teamId)

        team = self.client.get_team(teamId)

        if not team:
            raise ValueError(f"Không tìm thấy dữ liệu đội bóng: {teamId}")
        
        logger.info(
            "Đã lấy thành công dữ liệu đội bóng: %s",
            team.get("name")
        )
        return team
    
