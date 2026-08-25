with source as(
    select team_id, team_short_name,
        team_tla, area_id, team_founded,
        extracted_at   
    from {{ source('raw','teams') }}
),

stg_teams as (
    select 
        CAST(team_id AS INTEGER) AS team_id,
        TRIM(team_short_name) AS Name_of_team,
        UPPER(TRIM(team_tla)) AS TLA,
        CAST(area_id as integer) as area_id,
        CAST(team_founded AS integer) as founded_year,
        CAST(extracted_at AS TIMESTAMPTZ) AS extracted_at

        from source
)
select * from stg_teams


