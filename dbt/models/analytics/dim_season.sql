with season as (
    select
        season_id,
        competition_id,
        start_date,
        end_date
    from {{ ref('stg_season') }}
),
    competition as (
    select 
        competition_id,
        name_of_competition
    from {{ ref('stg_competition')}}
)

select s.season_id,
        s.start_date,
        s.end_date,
        c.name_of_competition
from season s
left join competition c on s.competition_id=c.competition_id

