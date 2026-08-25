with fact as (
    select * 
    from {{ ref('fact_matches_team')}}
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
        f.match_id,
        f.season_id,

        s.start_date,
        s.end_date,

        f.competition_id,
        c.name_of_competition,

        f.stage,
        f.home_team_id,
        home_team.Name_of_team as name_home_team,

        f.away_team_id,
        away_team.Name_of_team as name_away_team,

        f.winner_id,
        case 
            when f.winner_id=f.home_team_id then home_team.Name_of_team
            when f.winner_id=f.away_team_id then away_team.Name_of_team
        end as name_winner,


        f.duration,
        f.fulltime_home,
        f.fulltime_away,
        f.halftime_home,
        f.halftime_away,

        f.total_goals,
        f.match_narrative,
        f.is_over_2_5,
        f.higher_scoring_half,
        f.is_home_clean_sheet,
        f.is_away_clean_sheet,

        f.regulartime_home,
        f.regulartime_away,
        f.extratime_home,
        f.extratime_away,
        f.penalties_home,
        f.penalties_away
    
    from fact f 
    left join competition c on f.competition_id = c.competition_id
    
    left join season s on f.season_id = s.season_id
    left join team home_team on f.home_team_id = home_team.team_id
    left join team away_team on f.away_team_id = away_team.team_id
