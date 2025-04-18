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
            end as classification,
            case
                when source.patient_type = 1
                then 'returned_home'
                when source.patient_type = 2
                then 'hospitalized'
                else null
            end as patient_type,
            case
                when source.pneumonia in (99, 97) then null else source.pneumonia
            end as pneumonia,
            case
                when source.pregnant in (99, 97) then null else source.pregnant
            end as pregnancy,
            case
                when source.diabetes in (99, 97) then null else source.diabetes
            end as diabetes,
            case when source.copd in (99, 97) then null else source.copd end as copd,
            case
                when source.asthma in (99, 97) then null else source.asthma
            end as asthma,
            case
                when source.inmsupr in (99, 97) then null else source.inmsupr
            end as inmsupr,
            case
                when source.hipertension in (99, 97) then null else source.hipertension
            end as hypertension,
            case
                when source.cardiovascular in (99, 97)
                then null
                else source.cardiovascular
            end as cardiovascular,
            case
                when source.renal_chronic in (99, 97)
                then null
                else source.renal_chronic
            end as renal_chronic,
            case
                when source.other_disease in (99, 97)
                then null
                else source.other_disease
            end as other_disease,
            case
                when source.obesity in (99, 97) then null else source.obesity
            end as obesity,
            case
                when source.tobacco in (99, 97) then null else source.tobacco
            end as tobacco,
            source.usmer,
            source.medical_unit,
            case
                when source.intubed in (99, 97) then null else source.intubed
            end as intubed,
            case when source.icu in (99, 97) then null else source.icu end as icu,
            case
                when source.date_died = '9999-99-99' then null else date_died
            end as date_died
        from source
    )
select *
from id_label
