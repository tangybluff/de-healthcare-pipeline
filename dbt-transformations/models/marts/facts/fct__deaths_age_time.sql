{{ config(materialized="table") }}

-- How many monthly/yearly deaths by age group?
with

    -- Parse the date_died column
    parsed_patients as (
        select
            age_group,
            case
                when date_died = 'recovered'
                then null
                else parse_date('%d/%m/%Y', date_died)
            end as died_date
        from {{ ref("int__normalized_patients") }}
        where patient_type = 'hospitalized'  -- Filter for hospitalized patients
    ),

    -- Filter out recovered patients and extract month/year
    filtered_patients as (
        select
            age_group,
            extract(year from died_date) as year,
            extract(month from died_date) as month
        from parsed_patients
        where died_date is not null
    ),

    -- Count deaths by age group and month/year
    deaths_by_month as (
        select age_group, year, month, count(*) as deaths
        from filtered_patients
        group by age_group, year, month
    )

select *
from deaths_by_month
order by year, month, age_group
