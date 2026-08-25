with standing as (
    select * 
    from {{ ref('stg_standing')}}
),
    team as (
        select  team_id,Name_of_team
        from {{ ref('stg_teams')}}
    ),

    season as (
        select season_id,winner_team_id
        from {{ ref('stg_season')}}
    )

select 
    st.season_id,


    st.competition_id,


    st.position,

    st.team_id,


    st.form,
    st.won,
    st.draw,
    st.lost,
    st.points,
    st.goalsfor,
    st.goalsagainst,
    st.goaldifference, 
    
    (select 
        te.Name_of_team
    from team as te 
    where te.team_id = se.winner_team_id
    ) as champion_name

from standing st
left join team t on st.team_id = t.team_id
left join season se on st.season_id = se.season_id
left join team champ_team on se.winner_team_id = champ_team.team_id