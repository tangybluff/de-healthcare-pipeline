{{ config(materialized="table") }}

with

    normalized_patients as (select * from {{ ref("int__normalized_patients") }}),

    parsed_dates as (
        select
            case
                when date_died = 'recovered' then null else safe_cast(date_died as date)
            end as died_date
        from normalized_patients
    ),

    bounds as (
        select min(died_date) as min_date, max(died_date) as max_date from parsed_dates
    ),

    calendar as (
        select day
        from
            bounds,
            unnest(
                generate_date_array(
                    coalesce(min_date, date_sub(current_date(), interval 365 day)),
                    coalesce(max_date, current_date()),
                    interval 1 day
                )
            ) as day
    )

select
    day as date,
    extract(year from day) as year,
    format_date('%B', day) as month,  -- Full month name
    extract(day from day) as day_of_month,
    extract(week from day) as week_of_year,
    format_date('%A', day) as day_of_week  -- Full weekday name
from calendar
order by day
