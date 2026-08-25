with source as(
    select competition_id, season_id,
        player_id, team_id, goals,
        assists , penalties,
        extracted_at   
    from {{ source('raw','top_scorers') }}
),

stg_top_scorers as (
    select 
        CAST(competition_id as integer) as competition_id,
        CAST(season_id as integer) as season_id,
        CAST(player_id as integer) as player_id,
        
        CAST(team_id AS INTEGER) AS team_id,

        CAST(goals AS INTEGER) AS goals,
        CAST(assists AS INTEGER) AS assists,
        CAST(penalties AS INTEGER) AS penalties,
        CAST(extracted_at AS TIMESTAMPTZ) AS extracted_at

        from source
)
select *, row_number() over (
    partition by competition_id , season_id
    order by goals desc, player_id asc) as stt 

from stg_top_scorers 



