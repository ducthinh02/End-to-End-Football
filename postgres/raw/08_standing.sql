    CREATE TABLE raw.standing(
        season_id       integer not null,
        competition_id  integer not null,

        stage           text not null,
        standing_type   varchar(10) not null,

        position    SMALLINT,
        team_id        integer not null,
        
        playedGames     integer,

        form            text,
        won             integer,
        draw            integer,
        lost            integer,

        points          integer,

        goalsfor        integer,
        goalsAgainst    integer,
        goalDifference  integer,
        
        extracted_at TIMESTAMPTZ DEFAULT NOW(),
        primary key(season_id,competition_id,team_id,stage,standing_type )
    );