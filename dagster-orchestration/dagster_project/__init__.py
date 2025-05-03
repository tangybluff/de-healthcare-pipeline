from dagster import Definitions, load_assets_from_modules

from . import assets
from .schedules import covid_data_schedule

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    schedules=[covid_data_schedule],
)