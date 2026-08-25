from extract.players import PlayerExtractor
from extract.team import TeamExtractor

from .DatabaseConnection import DatabaseConnection

from loads.PlayerLoader import PlayerLoader
import logging

import time

logger = logging.getLogger(__name__)

class PlayerService(DatabaseConnection):
    
    def __init__(self, team_extractor: TeamExtractor,player_extractor: PlayerExtractor):
        super().__init__()
        self.team_extractor = team_extractor
        self.player_extractor = player_extractor

        self.list_person_id = []
    
    def extract_PlayerId(self):
        # ,"ELC","CL","PL","EC","FL1","BL1","SA","PD"
        competitions = ["WC"]
        
        loader = PlayerLoader(self.conn)  
        
        for competition in competitions:
                
                try:
                    teams = self.team_extractor.extract_teams_by_competition(competition)
                    if not teams:
                        raise ValueError(
                            f"No team data found for {competition}")
                    
                    list_teams:list[dict] = teams.get("teams",[])
                    
                    if not list_teams:
                        raise ValueError(
                            f"No teams found for competition: {competition}"
                        )
                    
                    list_team_id = []
                    
                    for team_list in list_teams:
                        
                        list_team_id.append(team_list.get("id"))
                                                
                    
                    self.get_player_id(list_team_id)
                    
                
                except Exception:
                    logger.info(
                        "Teams pipeline failed")
                    raise
        
        for person_Id in self.list_person_id:
            
            try:
                
                player = self.player_extractor.extract_player(person_Id)
                
                if not player:
                    
                    raise ValueError(
                        f"No player data found for {person_Id}")
                
                loader.load_player(player)
                
                self.conn.commit()
                logger.info(
                        "Player pipeline completed successfully."
                    )
                
                time.sleep(6)
                
            except Exception:
                self.conn.rollback(),
                logger.info(
                        "Player pipeline failed")
                raise    
        
    
    def get_player_id(self, list_team_id: list):
        
        if not list_team_id:
            raise ValueError("Data not found")
        
        
        for team_id in list_team_id:
            
            team = self.team_extractor.extract_team(team_id)
            
            squad = (
                team.get("squad",[])
            )
        
            for player in squad:
                
                player_id  = (
                    player.get("id")
                )
                
                if player_id  not in self.list_person_id:
                    self.list_person_id.append(player_id )
    