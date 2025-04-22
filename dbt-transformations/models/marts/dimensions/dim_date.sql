{{ config(materialized="table") }}

with

    -- 1) parse the date_died strings (or null for “recovered”)
    parsed_dates as (
        select
            case
                when date_died = 'recovered'
                then null
                else parse_date('%d/%m/%Y', date_died)
            end as died_date
        from {{ ref("int__normalized_patients") }}
    ),

    -- 2) find the bounds: earliest non-null died_date → today
    bounds as (
        select min(died_date) as min_date, current_date() as max_date from parsed_dates
    ),

    -- 3) generate one row per calendar day in that range
    calendar as (
        select day
        from
            bounds,
            unnest(generate_date_array(min_date, max_date, interval 1 day)) as day
    )

select
    day as date,
    extract(year from day) as year,
    format_date('%B', day) as month,  -- e.g. “June”
    extract(day from day) as day_of_month,
    extract(week from day) as week_of_year,
    format_date('%A', day) as day_of_week  -- e.g. “Monday”
from calendar
order by day
