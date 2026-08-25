with source as (
    select season_id, competition_id,
        start_date, end_date, 
        winner_team_id

    from {{source('raw','season')}}
    ),

stg_season as (
    
    select
        cast(season_id as integer) as season_id,
        cast(competition_id as integer) as competition_id,
        cast(start_date as date) as start_date,
        cast(end_date as date) as end_date,
        cast(winner_team_id as integer) as winner_team_id
    from source
    
)
select * from stg_season