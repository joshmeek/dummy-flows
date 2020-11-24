# start with start date
# calculate weeks since
# ship it

# from prefect import Flow, task

from prefect import Flow, task

import pendulum



def notif(tracked_obj, old_state, new_state):
    from prefect import context
    print(context.flow_name)
    if new_state.is_successful():
        print(new_state.result)

    return new_state

@task(state_handlers=[notif])
def a():
    return 1234

@task
def b(x):
    print(x)

with Flow("test") as flow:
    a = a()
    b = b(a)

flow.run()