# start with start date
# calculate weeks since
# ship it

# from prefect import Flow, task

from prefect import Flow, task
from prefect.client import Secret
from prefect.utilities.notifications import slack_message_formatter
from prefect.schedules.clocks import CronClock
from prefect.schedules import Schedule

from typing import cast

import pyfiglet
import pendulum
import requests


def test_slack(tracked_obj, old_state, new_state):

    if new_state.is_successful():
        webhook_url = cast(str, Secret("SLACK_WEBHOOK_URL").get())

        form_data = {
            "attachments": [
                {
                    "color": "#FB4179",
                    "author_name": "not lauren and josh",
                    "author_icon": "https://emojis.slackmojis.com/emojis/images/1466642201/535/celebrate.gif",
                    "title": "Welcome to Week",
                    "fields": [],
                    "text": "```{}```".format(
                        pyfiglet.figlet_format(str(new_state.result), font="small")
                    ),
                }
            ]
        }

        # form_data = slack_message_formatter(tracked_obj, new_state)
        r = requests.post(webhook_url, json=form_data)
        if not r.ok:
            raise ValueError("Slack notification for {} failed".format(tracked_obj))

    return new_state


@task
def get_start_date():
    return pendulum.naive(2018, 1, 17)


@task(state_handlers=[test_slack])
def calculate_weeks_since(start_date):
    current_date = pendulum.now().naive()
    return current_date.diff(start_date).in_weeks()


with Flow(
    "weeks-since",
    schedule=Schedule(
        clocks=[CronClock("30 11 * * 1", start_date=pendulum.now("America/Toronto"))]
    ),
) as flow:
    start_date = get_start_date()
    calculate_weeks_since(start_date)

# flow.run(run_on_schedule=False)
flow.register(project_name="Demo")
