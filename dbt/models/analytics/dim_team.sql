with teams as (
    select
        team_id,
        Name_of_team,
        TLA,
        area_id,
        founded_year
    from {{ ref('stg_teams')}}
), 
    areas as (
        select 
            area_id,
            area_name
        
        from {{ ref('stg_areas')}}
    )

select 
    t.team_id,
    t.Name_of_team,
    t.TLA,
    a.area_name,
    t.founded_year
from teams t 
left join areas a on t.area_id = a.area_id