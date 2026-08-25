select 
    season_id,
    competition_id,
    team_id,
    
    position,
    form,
    won,
    draw,
    lost,
    points,
    goalsfor,
    goalsagainst,
    goaldifference,
    champion_name
from {{ ref('int_team_performance')}}