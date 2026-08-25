from src.api.Football_Client import FootballClient

class BaseExtractor:
    
    def __init__(self):
        self.client = FootballClient()
    