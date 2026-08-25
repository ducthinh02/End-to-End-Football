with source as(
    select team_id, competition_id,
        season_id, 
        extract_at   
    from {{ source('raw','team_competition') }}
),

stg_team_competition as (
    select 
        CAST(team_id AS INTEGER) AS team_id,
        CAST(competition_id as integer) as competition_id,
        CAST(season_id as integer) as season_id,
        CAST(extract_at AS TIMESTAMPTZ) AS extract_at

        from source
)
select * from stg_team_competition


