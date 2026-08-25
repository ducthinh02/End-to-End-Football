with competition as (
    select 
        competition_id,
        name_of_competition,
        code_of_competition,
        TYPE_OF_COMPETITION,
        area_id
    
    from {{ ref('stg_competition')}}
),
    areas as (
        select 
            area_id,
            area_name
        
        from {{ ref('stg_areas')}}
    )

select 
    competition_id,
    name_of_competition,
    code_of_competition,
    TYPE_OF_COMPETITION,
    area_name

from competition c
left join areas a on c.area_id=a.area_id