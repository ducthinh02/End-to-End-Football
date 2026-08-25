CREATE TABLE raw.teams (

    team_id INTEGER PRIMARY KEY, 

    team_name TEXT  NOT NULL,
    team_short_name text,
    team_tla Varchar(3) NOT NULL,

    team_crest  text,

    area_id     INTEGER NOT NULL,

    team_address text,
    team_website text,

    team_founded   SMALLINT CHECK(team_founded BETWEEN 1800 AND 2026) ,
    team_venue  text ,

    api_last_updates    TIMESTAMPTZ,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);