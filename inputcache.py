import datetime
import random

from prefect.engine.cache_validators import all_inputs
from prefect import task, Flow, Parameter


@task(cache_for=datetime.timedelta(minutes=5, seconds=30), cache_validator=all_inputs)
def return_random_number(x):
    return random.randint(0, x)


@task
def print_number(num):
    print("=" * 50)
    print("Value: {}".format(num))
    print("=" * 50)


with Flow("cached-task") as flow:
    x = Parameter("x")
    num = return_random_number(x)
    result = print_number(num)
