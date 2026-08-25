with matches as (
    select 
        match_id,
        season_id,
        competition_id,
        stage,
        home_team_id,
        away_team_id,
        winner,
        duration,
        fulltime_home,
        fulltime_away,
        halftime_home,
        halftime_away,
        regulartime_home,
        regulartime_away,
        extratime_home,
        extratime_away,
        penalties_home,
        penalties_away,  

        coalesce(fulltime_home, 0) + coalesce(fulltime_away, 0) as total_goals,

        case 
            when coalesce(halftime_home, 0) < coalesce(halftime_away, 0) and coalesce(fulltime_home, 0) > coalesce(fulltime_away, 0) then 'Home Comeback'
            when coalesce(halftime_home, 0) > coalesce(halftime_away, 0) and coalesce(fulltime_home, 0) < coalesce(fulltime_away, 0) then 'Away Comeback'
            when coalesce(halftime_home, 0) > coalesce(halftime_away, 0) and coalesce(fulltime_home, 0) <= coalesce(fulltime_away, 0) then 'Home Bottled'
            when coalesce(halftime_home, 0) < coalesce(halftime_away, 0) and coalesce(fulltime_home, 0) >= coalesce(fulltime_away, 0) then 'Away Bottled'
            else 'Standard'
        end as match_narrative,

        case 
            when (coalesce(fulltime_home, 0) + coalesce(fulltime_away, 0)) > 2.5 then 'Over 2.5'
            else 'Under 2.5'
        end as is_over_2_5,

        case 
            when (coalesce(fulltime_home, 0) - coalesce(halftime_home, 0) + coalesce(fulltime_away, 0) - coalesce(halftime_away, 0)) > (coalesce(halftime_home, 0) + coalesce(halftime_away, 0)) 
                then '2nd Half'
            when (coalesce(fulltime_home, 0) - coalesce(halftime_home, 0) + coalesce(fulltime_away, 0) - coalesce(halftime_away, 0)) < (coalesce(halftime_home, 0) + coalesce(halftime_away, 0)) 
                then '1st Half'
            else 'Equal'
        end as higher_scoring_half, 

        case when coalesce(fulltime_away, 0) = 0 then 1 else 0 end as is_home_clean_sheet,
        case when coalesce(fulltime_home, 0) = 0 then 1 else 0 end as is_away_clean_sheet

    from {{ ref('stg_matches') }}
)

select 
    m.match_id,
    m.season_id,
    m.competition_id,
    m.stage,
    m.home_team_id,
    m.away_team_id,

    case
        when m.winner = 'HOME_TEAM' then m.home_team_id
        when m.winner = 'AWAY_TEAM' then m.away_team_id
        else null
    end as winner_id,

    m.duration,
    m.fulltime_home,
    m.fulltime_away,
    m.halftime_home,
    m.halftime_away,

    m.total_goals,
    m.match_narrative,
    m.is_over_2_5,
    m.higher_scoring_half,
    m.is_home_clean_sheet,
    m.is_away_clean_sheet,

    m.regulartime_home,
    m.regulartime_away,
    m.extratime_home,
    m.extratime_away,
    m.penalties_home,
    m.penalties_away

from matches as m