import random
from prefect.triggers import all_successful, all_failed
from prefect import task, Flow

@task(name="Task A")
def task_a():
    rand_num = float(random.random())
    curr_limits = float(0.5)
    if rand_num < curr_limits:
        raise ValueError(f'{rand_num} is less than {curr_limits}')
    return rand_num

@task(name="Task 2")
def task_2():
    rand_num = float(random.random())
    curr_limits = float(0.5)
    if rand_num < curr_limits:
        raise ValueError(f'{rand_num} is less than {curr_limits}')
    return rand_num

@task(name="Task B", trigger=all_successful)
def task_b(v):
    print(v)

@task(name="Task C", trigger=all_failed)
def task_c(v):
    print("Failed")

with Flow('My triggers') as flow:
    rn = task_a()
    rn2 = task_a()
    success = task_b([task_a, task_a])
    fail = task_c(rn)

# flow.set_reference_tasks([success])
flow_state = flow.run()