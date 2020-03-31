from prefect import task, Flow
from prefect.tasks.control_flow import switch


@task
def start():
    print("starting...")


@task
def a_task():
    print("aaaaa!")


@task(skip_on_upstream_skip=False)
def b_task():
    print("bbbb!")


@task
def c_task():
    print("CCCCCC!")


@task
def check1():
    result = False
    print("check1", result)
    return result


@task
def check2():
    result = False
    print("check2", result)
    return result


@task(skip_on_upstream_skip=False)
def finish():
    print("finish!")


with Flow("My Flow") as flow:
    conditionally_run_a = switch(check1, {True: a_task})
    conditionally_run_c = switch(check2, {True: b_task})
    flow.chain(start, a_task, b_task, c_task, finish)

flow.run()
