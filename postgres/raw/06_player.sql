CREATE TABLE raw.player(
    player_id   integer PRIMARY KEY,

    player_name     text,
    player_firstName text,
    player_lastName  text,

    date_of_birth   date,
    nationality     text,

    position    text,
    shirt_number    integer,
    
    api_last_update TIMESTAMPTZ,
    extracted_at      TIMESTAMPTZ not null DEFAULT NOW()
);