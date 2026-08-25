CREATE TABLE raw.season (
    season_id      INTEGER ,
    competition_id INTEGER,
    start_date     DATE,
    end_date       DATE,
    currentMatchday SMALLINT,
    winner_team_id INTEGER,
    stages         text,

    PRIMARY KEY(season_id,competition_id)
);