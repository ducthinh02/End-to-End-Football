with fact as (
    select *
    from {{ ref('fact_team_performance')}}
),
    competition as (
        select *
        from {{ ref('dim_competition')}}
    ),
    team as (
        select *
        from {{ ref('dim_team')}}

    ),
    season as (
        select *
        from {{ ref('dim_season')}}
    )
    
    select 
        f.season_id,
        s.start_date,
        s.end_date,
    
        f.competition_id,
        c.name_of_competition,
        c.code_of_competition,
        c.TYPE_OF_COMPETITION,

        f.team_id,
        t.Name_of_team,
        t.TLA,
        t.area_name,
        t.founded_year,
        
        f.position,
        f.form,
        f.won,
        f.draw,
        f.lost,
        f.points,
        f.goalsfor,
        f.goalsagainst,
        f.goaldifference,
        f.champion_name

    from fact f
    left join competition c on f.competition_id = c.competition_id
    left join team t on f.team_id = t.team_id
    left join season s on f.season_id = s.season_id