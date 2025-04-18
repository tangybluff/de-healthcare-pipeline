with

    source as (select * from {{ source("covid19_dataset", "covid_data_from_gcs") }}),

    id_label as (
        select
            row_number() over () as patient_id,
            case
                when source.sex = 1
                then 'female'
                when source.sex = 2
                then 'male'
                else null
            end as sex,
            source.age,
            case
                when source.clasiffication_final between 1 and 3
                then 'diagnosed'
                when source.clasiffication_final >= 4
                then 'not_carrier_or_inconclusive'
                else null
            end as clasiffication_final,
            case
                when source.patient_type = 1
                then 'returned_home'
                when source.patient_type = 2
                then 'hospitalized'
                else null
            end as patient_type,
            nullif(source.pneumonia, 99) as pneumonia,
            nullif(source.pregnant, 99) as pregnancy,
            nullif(source.diabetes, 99) as diabetes,
            nullif(source.copd, 99) as copd,
            nullif(source.asthma, 99) as asthma,
            nullif(source.inmsupr, 99) as inmsupr,
            nullif(source.hipertension, 99) as hypertension,
            nullif(source.cardiovascular, 99) as cardiovascular,
            nullif(source.renal_chronic, 99) as renal_chronic,
            nullif(source.other_disease, 99) as other_disease,
            nullif(source.obesity, 99) as obesity,
            nullif(source.tobacco, 99) as tobacco,
            source.usmer,
            source.medical_unit,
            nullif(source.intubed, 99) as intubed,
            nullif(source.icu, 99) as icu,
            case
                when source.date_died = '9999-99-99' then null else date_died
            end as date_died
        from source
    )
select *
from id_label
