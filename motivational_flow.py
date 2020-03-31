from datetime import datetime
import random

import pendulum
import requests
from bs4 import BeautifulSoup

from prefect import task, Flow
from prefect.client import Secret
from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock
from prefect.environments.storage import Docker

req = requests.get("https://personaldevelopfit.com/motivational-quotes/")
content = BeautifulSoup(req.content, features="lxml")
quote_ordered_list = content.find("ol")
quote_list = [x.text for x in quote_ordered_list.find_all("strong")]


@task
def get_content():
    req = requests.get("https://personaldevelopfit.com/motivational-quotes/")
    return req.content


@task
def get_quote_list(content):
    content = BeautifulSoup(content, features="lxml")
    quote_ordered_list = content.find("ol")
    return [x.text for x in quote_ordered_list.find_all("strong")]


@task
def get_random_quote(quote_list):
    random_index = random.randint(0, 499)
    return quote_list[random_index]


@task
def post_to_slack(quote):
    print(quote)
    # WEBHOOK = Secret("SLACK_WEBHOOK_URL").get()
    # r = requests.post(WEBHOOK, json={"text": quote})
    # r.raise_for_status()


with Flow(
    "motivational-flow",
    schedule=Schedule(
        clocks=[CronClock("0 8 * * 1-5", start_date=pendulum.now(tz="US/Pacific"))],
    ),
    storage=Docker(
        registry_url="joshmeek18",
        image_name="flows",
        python_dependencies=["bs4", "lxml", "requests"],
    ),
) as flow:
    content = get_content()
    quote_list = get_quote_list(content)
    random_quote = get_random_quote(quote_list)
    post_to_slack(random_quote)

flow.run(run_on_schedule=False)
# flow.register(project_name="Motivation")
# print(datetime.fromtimestamp(pendulum.now(tz="US/Pacific").timestamp()))
# Schedule(
#     # emit an event every hour
#     clocks=[IntervalSchedule(interval=timedelta(hours=1))]
