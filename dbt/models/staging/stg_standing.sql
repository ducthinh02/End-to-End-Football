with source as(
    select season_id, competition_id,
        stage, standing_type,
        position, team_id, form,
        won, draw, lost, points,
        goalsfor, goalsagainst, goaldifference, 
        extracted_at   
    from {{ source('raw','standing') }}
),

stg_standing as (
    select 
        CAST(season_id as integer) as season_id,
        CAST(competition_id as integer) as competition_id,
        upper(trim(stage)) as stage,
        upper(trim(standing_type)) as standing_type,
        
        
        CAST(position AS INTEGER) AS position,
        CAST(team_id AS INTEGER) AS team_id,

        upper(trim(form)) as form,

        CAST(won AS INTEGER) AS won,
        CAST(draw AS INTEGER) AS draw,
        CAST(lost AS INTEGER) AS lost,
        CAST(points AS INTEGER) AS points,
        CAST(goalsfor AS INTEGER) AS goalsfor,
        CAST(goalsagainst AS INTEGER) AS goalsagainst,
        CAST(goaldifference AS INTEGER) AS goaldifference,
        
        CAST(extracted_at AS TIMESTAMPTZ) AS extracted_at

        from source
)
select * from stg_standing


