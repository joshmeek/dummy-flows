from prefect import Flow, task, Parameter
from prefect.tasks.control_flow import case, merge


@task
def if_option_a():
    pass


@task
def if_option_b():
    pass


@task
def some_additional_step(temp):
    pass


@task
def some_final_step(x):
    pass


with Flow("case-based-flow") as flow:
    option = Parameter("option")

    with case(option, "a"):
        temp = if_option_a()
        x_a = some_additional_step(temp)

    with case(option, "b"):
        x_b = if_option_b()

    x = merge(x_a, x_b)
    output = some_final_step(x)

flow.register()
