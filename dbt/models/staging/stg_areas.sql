with source as(
    select * from {{ source('raw','areas') }}
),

stg_areas as (
    select 
        CAST(area_id AS INTEGER) AS area_id,
        TRIM(area_name) AS area_name,
        UPPER(TRIM(area_code)) AS area_code,
        CAST(parent_area_id as integer) as parent_area_id,
        TRIM(parent_area_name) as parent_area_name,
        CAST(extract_at AS TIMESTAMPTZ) AS extract_at

        from source
)
select * from stg_areas


