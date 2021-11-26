from prefect import task

from .fetch_from_api import fetch as fetch_from_api
from .save_to_csv import save as save_to_csv

@task
def extract(info):
    return fetch_from_api(info)

@task
def load(info, items):
    save_to_csv(info, items)

