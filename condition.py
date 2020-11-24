from random import random

from prefect import task, Flow, case
from testtask import testtask

@task
def check_condition():
    return False

@task
def action_if_true():
    return "I am true!"

@task
def another_action(val):
    print(val)


with Flow("conditional-branches") as flow:
    cond = check_condition()

    with case(cond, True):
        val = action_if_true()
        another_action(val)

        t = testtask()

flow.register(project_name="Demo")