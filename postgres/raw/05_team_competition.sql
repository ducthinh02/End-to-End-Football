    CREATE TABLE raw.team_competition(
            team_id INTEGER NOT NULL,

            competition_id INTEGER NOT NULL,
            
            season_id INTEGER NOT NULL,

            extract_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            coach_id    INTEGER,
            coach_name  text,

        PRIMARY KEY(team_id, competition_id)

    );