with source as(
    select player_id, player_name,
        date_of_birth, nationality,
        position, shirt_number,
        extracted_at   
    from {{ source('raw','player') }}
),

stg_player as (
    select 
        CAST(player_id AS INTEGER) AS player_id,
        TRIM(player_name) AS Name_of_player,
        cast(date_of_birth as date) as Birth,
        
        UPPER(TRIM(nationality)) AS nationality,

        UPPER(TRIM(position)) AS position,
        CAST(shirt_number as integer) as shirt_number,
        CAST(extracted_at AS TIMESTAMPTZ) AS extracted_at

        from source
)
select * from stg_player


