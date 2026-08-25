CREATE TABLE raw.competition(
    competition_id  INTEGER PRIMARY KEY,

    area_id INTEGER NOT NULL,

    competition_name    text,
    competition_code    text,

    competition_type    varchar(10),
    competition_emblem  text DEFAULT NULL,
    
    current_season_id   INTEGER not null,
    number_of_available_seasons integer,
    
    api_last_update     TIMESTAMP,
    extract_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);