{{ config(materialized="table") }}

-- How many patients recovered by risk level and age group?
select
    risk_level,
    age_group,
    count(*) as total_patients,
    sum(case when date_died = 'recovered' then 1 else 0 end) as num_recovered
from {{ ref("int__normalized_patients") }}
group by risk_level, age_group
order by risk_level, age_group
