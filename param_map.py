import random

import prefect
from prefect import task, Flow, Parameter, unmapped


@task
def generate_numbers(max_num, amount):
    return random.sample(range(max_num), amount)


@task
def multiply(number, multiple):
    if number % 10 == 0:
        raise prefect.engine.signals.FAIL
    return number * multiple


@task
def summation(numbers):
    print(sum(numbers))


with Flow("random-numbers") as flow:
    max_num = Parameter("max_num", default=10)
    amount = Parameter("amount", default=10)
    multiple = Parameter("multiple", default=10)

    numbers = generate_numbers(max_num, amount)
    multiples = multiply.map(numbers, multiple=unmapped(multiple))

    summation(multiples)

flow.environment = prefect.environments.RemoteEnvironment(executor="prefect.engine.executors.DaskExecutor")

flow.register(project_name="Demo")
# flow.run(parameters={"max_num": 100, "amount": 100, "multiple": 50})
