import requests 
from src.api.auth import (
    API_BASE_URL, 
    HEADERS,
    TIMEOUT
)
import logging  
from src.api import endpoints
from typing import Optional
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)

class FootballClient:
    
    """Class dùng để giao tiếp với football-data.org"""

    def __init__(self):
        self.base_url = API_BASE_URL
        self.headers = HEADERS
        self.timeout = TIMEOUT
        self.session = requests.Session()
        
        retry_strategy = Retry(
        total=5,  # Thử lại tối đa 5 lần
        backoff_factor=6,  # Thời gian chờ tăng dần: lần 1 ~6s, lần 2 ~12s, lần 3 ~24s...
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],  # Các mã lỗi kích hoạt cơ chế tự động gọi lại
        allowed_methods=["GET"],  # Chỉ áp dụng cho phương thức GET
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _request(self, 
                endpoint :str ,
                params: Optional[dict] = None) ->dict:
        

        url = self.base_url + endpoint

        logger.info("GET %s", url)
        try:
            response = self.session.get(
                url=url,
                params= params,
                headers= self.headers,
                timeout= self.timeout
            )


            response.raise_for_status()
        
            logger.info(
                "Success %s %s",
                response.status_code,
                url
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Request failed: %s", e)
            raise


#====================================================
# Lấy data từ endpoint và gán vào _request
#  để call api lấy dữ liệu
# ===========================================


    # ENDPOINT ĐỘI BÓNG
    def get_team(self,team_id):
        endpoint = endpoints.TEAM.format(team_id = team_id)
        return self._request(endpoint)
    
    def get_team_ForCompetitions(self,code):
        endpoint = endpoints.TEAMS_FOR_COMPETITIONS.format(code = code)
        return self._request(endpoint)

    
    # ENDPOINT TT TRẬN ĐẤU
    def get_matches(self,match_id): 
        endpoint = endpoints.MATCH.format(match_id= match_id)
        return self._request(endpoint)

    def get_competition_matches(self, code):
        endpoint = endpoints.MATCHES.format(code = code)
        return self._request(endpoint)


    # ENDPOINT BXH
    def get_standing(self,code, season=None):
        endpoint = endpoints.STANDINGS.format(code = code)
        params = None
        if season is None:
            params ={
                "season":season
            }
        return self._request(endpoint=endpoint,
                            params=params)
    
    
    # ENDPOINT KHU VỰC
    def get_area(self):
        endpoint = endpoints.AREAS.format()
        return self._request(endpoint)
    

    # ENDPOINT GIẢI ĐẤU
    def get_competition(self):
        endpoint = endpoints.COMPETITION
        return self._request(endpoint)
    
    def get_competition_for_code(self,code):
            endpoint = endpoints.COMPETITION_FOR_CODE.format(code=code)
            return self._request(endpoint)
    
    
    # ENDPOINT CẦU THỦ XUẤT SẮC
    def get_topScorers(self,code):
        endpoint = endpoints.TOP_SCORERS.format(code = code)
        return self._request(endpoint)
    
    # ENDPOINT THÔNG TIN CẦU THỦ
    def get_player(self,person_id): 
        endpoint = endpoints.PLAYER.format(person_id = person_id)
        return self._request(endpoint)