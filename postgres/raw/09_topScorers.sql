create table raw.Top_scorers(
    competition_id integer,
    season_id      integer,
    player_id      integer, 
    team_id        integer,

    goals          smallint,
    assists        smallint,
    penalties      smallint,
    
    api_last_update timestamptz,
    extracted_at    timestamptz not null default now(),

    primary key(competition_id,season_id,player_id)

);