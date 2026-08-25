with source as(
    select competition_id, competition_name, competition_code,
        competition_type, current_season_id, extract_at,area_id

    
    from {{source('raw','competition')}}
),

stg_competition as(
    select 
        cast(competition_id as integer) as competition_id,
        trim(competition_name) AS name_of_competition,
        UPPER(TRIM(competition_code)) AS code_of_competition,
        Upper(trim(competition_type)) as TYPE_OF_COMPETITION,
        cast(current_season_id as integer) as season_id,
        cast(area_id as integer) as area_id,
        CAST(extract_at AS TIMESTAMPTZ) AS extract_at
    from source
)
select * from stg_competition