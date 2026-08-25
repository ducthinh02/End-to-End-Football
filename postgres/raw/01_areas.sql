CREATE TABLE raw.areas (
    area_id INTEGER PRIMARY KEY,

    area_name text,
    area_code varchar(5), 

    parent_area_id INTEGER,
    parent_area_name    text,
    
    extract_at      TIMESTAMPTZ DEFAULT NOW() 
);