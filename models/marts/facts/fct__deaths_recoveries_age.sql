{{ config(materialized="table") }}

-- How many patients by type died and recovered?
with
    base as (
        select
            patient_type,
            case when date_died = 'recovered' then 0 else 1 end as died_flag
        from {{ ref("int__normalized_patients") }}
    ),

    agg as (
        select patient_type, count(*) as total_patients, sum(died_flag) as num_died
        from base
        group by patient_type
    ),

    final as (
        select
            patient_type,
            total_patients,
            num_died,
            total_patients - num_died as num_recovered
        from agg
    )

select *
from final
