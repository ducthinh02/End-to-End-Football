with source as (
    select match_id, season_id,
    competition_id, match_status,
    stage, home_team_id, away_team_id,
    winner, duration, fulltime_home, 
    fulltime_away, halftime_home,
    halftime_away, regulartime_home,
    regulartime_away, extratime_home,
    extratime_away, penalties_home,
    penalties_away, extracted_at

    from {{ source('raw','matches')}}

    ),

stg_matches as (
    select
        cast(match_id as integer) as match_id,
        cast(season_id as integer) as season_id,
        cast(competition_id as integer) as competition_id,
        upper(trim(match_status)) as match_status,
        upper(trim(stage)) as stage,
        cast(home_team_id as integer) as home_team_id,
        cast(away_team_id as integer) as away_team_id,
        upper(trim(winner)) as winner,
        upper(trim(duration)) as duration,

        cast(fulltime_home as integer) as fulltime_home,
        cast(fulltime_away as integer) as fulltime_away,
        cast(halftime_home as integer) as halftime_home,
        cast(halftime_away as integer) as halftime_away,
        cast(regulartime_home as integer) as regulartime_home,
        cast(regulartime_away as integer) as regulartime_away,
        cast(extratime_home as integer) as extratime_home,

        cast(extratime_away as integer) as extratime_away,
        cast(penalties_home as integer) as penalties_home,

        cast(penalties_away as integer) as penalties_away,
        cast(extracted_at as timestamp) as extracted_at

    from source
)
    select * from stg_matches