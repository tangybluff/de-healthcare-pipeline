{{ config(materialized="table") }}

with

    patient_data as (select * from {{ ref("stg_silver__patients") }}),

    normalized as (
        select
            patient_id,

            sex,
            age,

            -- 2) classification → covid_classification
            case
                when classification = 'diagnosed'
                then 'positive_diag'
                when classification = 'not_carrier_or_inconclusive'
                then 'inconclusive'
                else null
            end as covid_classification,

            patient_type,

            -- 1) drop medical_unit, usmer by simply omitting them
            -- 3) map 1/2 → YES/NO, and 4) nulls → NO
            case when pneumonia = 1 then 'YES' else 'NO' end as pneumonia,
            case when pregnancy = 1 then 'YES' else 'NO' end as pregnancy,
            case when diabetes = 1 then 'YES' else 'NO' end as diabetes,
            case when copd = 1 then 'YES' else 'NO' end as copd,
            case when asthma = 1 then 'YES' else 'NO' end as asthma,
            case when inmsupr = 1 then 'YES' else 'NO' end as inmsupr,
            case when hypertension = 1 then 'YES' else 'NO' end as hypertension,
            case when cardiovascular = 1 then 'YES' else 'NO' end as cardiovascular,
            case when renal_chronic = 1 then 'YES' else 'NO' end as renal_chronic,
            case when other_disease = 1 then 'YES' else 'NO' end as other_disease,
            case when obesity = 1 then 'YES' else 'NO' end as obesity,
            case when tobacco = 1 then 'YES' else 'NO' end as tobacco,
            case when intubed = 1 then 'YES' else 'NO' end as intubed,
            case when icu = 1 then 'YES' else 'NO' end as icu,

            -- 5) date_died NULL → 'recovered'
            case
                when date_died is null then 'recovered' else cast(date_died as string)
            end as date_died

        from patient_data
    )

select *
from normalized
