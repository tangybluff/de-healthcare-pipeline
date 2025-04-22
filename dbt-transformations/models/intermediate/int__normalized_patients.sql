{{ config(materialized="table") }}

with

    patient_data as (select * from {{ ref("stg_silver__patients") }}),

    normalized as (
        select
            patient_id,
            sex,
            age,
            -- Create an age group column
            case
                when age < 19
                then '0-18'
                when age between 19 and 30
                then '19-30'
                when age between 31 and 45
                then '31-45'
                when age between 46 and 60
                then '46-60'
                else '61+'
            end as age_group,

            -- Normalize covid classification
            case
                when classification = 'diagnosed'
                then 'positive_diag'
                when classification = 'not_carrier_or_inconclusive'
                then 'inconclusive'
                else null
            end as covid_classification,

            patient_type,

            -- Recode Boolean fields: 1 becomes 'YES' and any other value becomes 'NO'
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

            -- For date_died, if the value is null it indicates recovery
            case
                when date_died is null then 'recovered' else cast(date_died as string)
            end as date_died,

            /* Calculate risk_level:
               1. If either icu or intubed is 1, then 'extreme_risk'
               2. Otherwise, if the sum of comorbidities (diabetes, hypertension, copd, obesity)
                  from the raw data is greater than 2 then 'high_risk'
               3. Else, 'low_risk'
            */
            case
                when patient_data.icu = 1 or patient_data.intubed = 1
                then 'extreme_risk'
                when
                    (
                        (case when patient_data.copd = 1 then 1 else 0 end)
                        + (case when patient_data.pneumonia = 1 then 1 else 0 end)
                        + (case when patient_data.asthma = 1 then 1 else 0 end)
                        + (case when patient_data.tobacco = 1 then 1 else 0 end)
                    )
                    > 2
                then 'high_risk'
                else 'low_risk'
            end as risk_level

        from patient_data
    )

select *
from normalized
