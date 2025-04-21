{{ config(materialized="table") }}

with

    -- Prepare data for comorbidities and outcomes
    comorbidity_data as (
        select
            patient_id,
            age_group,
            risk_level,
            -- Count the number of comorbidities for each patient
            (
                (case when diabetes = 'YES' then 1 else 0 end)
                + (case when hypertension = 'YES' then 1 else 0 end)
                + (case when copd = 'YES' then 1 else 0 end)
                + (case when obesity = 'YES' then 1 else 0 end)
                + (case when asthma = 'YES' then 1 else 0 end)
                + (case when cardiovascular = 'YES' then 1 else 0 end)
                + (case when renal_chronic = 'YES' then 1 else 0 end)
                + (case when other_disease = 'YES' then 1 else 0 end)
            ) as num_comorbidities,
            -- Outcome: recovered or died
            case
                when date_died = 'recovered' then 'recovered' else 'died'
            end as outcome
        from {{ ref("int__normalized_patients") }}
    ),

    -- Aggregate data by comorbidities and outcomes
    aggregated_data as (
        select num_comorbidities, outcome, count(*) as patient_count
        from comorbidity_data
        group by num_comorbidities, outcome
    )

select *
from aggregated_data
order by num_comorbidities, outcome
