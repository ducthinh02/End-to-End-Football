    CREATE TABLE raw.matches(
        match_id        integer primary key,
        
        season_id       integer,
        competition_id  integer,

        utcDate         timestamptz,
        match_status    varchar(25),
        match_day       smallint,
        stage           text,

        home_team_id    integer,
        away_team_id    integer,

        winner          varchar(15),
        duration        varchar(30),

        fullTime_home   smallint,
        fullTime_away   smallint,

        halfTime_home   smallint,
        halfTime_away   smallint,

        regularTime_home smallint,
        regularTime_away smallint,

        extraTime_home  smallint,
        extraTime_away smallint,

        penalties_home  smallint,
        penalties_away  smallint,

        api_last_update timestamptz,
        extracted_at    timestamptz not null default now()
        );