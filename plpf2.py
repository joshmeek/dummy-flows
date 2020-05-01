from prefect import task, Flow
from prefect.engine.signals import FAIL
from prefect.environments import RemoteEnvironment
from prefect.triggers import all_successful, any_successful

# ---------------------
# Level 1
# ---------------------
# Check Stream Data Tasks
@task
def check_dl1_stream():
    return True


@task
def check_dl2_stream():
    return False


@task
def check_dl3_stream():
    return True


@task
def check_dl4_stream():
    return False


# Loading Dimension Tasks
@task
def load_dl1(exists):
    if exists:
        print("Loaded DL1 Data!")
    raise FAIL


@task
def load_dl2(exists):
    if exists:
        print("Loaded DL2 Data!")


@task
def load_dl3(exists):
    if exists:
        print("Loaded DL3 Data!")


@task
def load_dl4(exists):
    if exists:
        print("Loaded DL4 Data!")


# Check on Level 1 left and right tasks
@task(trigger=any_successful)
def check_level_1_left():
    print("Level 1 left is good!")


@task(trigger=all_successful)
def check_level_1_right():
    print("Level 1 right is good!")


# ---------------------
# Level 2
# ---------------------
# Check Stream Data Tasks
@task
def check_fl1_stream():
    return True


@task
def check_fl2_stream():
    return False


@task
def check_fl3_stream():
    raise FAIL
    return True


@task
def check_fl4_stream():
    return False


@task
def check_fl5_stream():
    return False


# Load Fact Tasks
@task
def fact_load_1(exists):
    if exists:
        print("Loaded FL1! Data!")


@task
def fact_load_2(exists):
    if exists:
        print("Loaded FL2! Data!")


@task
def fact_load_3(exists):
    if exists:
        print("Loaded FL3! Data!")


@task
def fact_load_4(exists):
    if exists:
        print("Loaded FL4! Data!")


@task
def fact_load_5(exists):
    if exists:
        print("Loaded FL5! Data!")


# Check on Level 2 left and right tasks
@task(trigger=any_successful)
def check_level_2_left():
    print("Level 2 left is good!")


@task(trigger=any_successful)
def check_level_2_right():
    print("Level 2 right is good!")


# ---------------------
# Level 3
# ---------------------
# Check Stream Data Tasks
@task
def check_af1_stream():
    return True


@task
def check_af2_stream():
    return False


@task
def check_af3_stream():
    raise FAIL
    return True


@task
def check_af4_stream():
    return False


# Load Agg Fact Tasks
@task
def agg_fact_load_1(exists):
    if exists:
        print("Loaded Agg Fact 1! Data!")


@task
def agg_fact_load_2(exists):
    if exists:
        print("Loaded Agg Fact 2! Data!")


@task
def agg_fact_load_3(exists):
    if exists:
        print("Loaded Agg Fact 3! Data!")


@task
def agg_fact_load_4(exists):
    if exists:
        print("Loaded Agg Fact 4! Data!")


# Check all at end
@task(trigger=any_successful)
def check_success():
    print("Level 3 is good!")


@task(trigger=any_successful)
def check_fail():
    print("Level 3 is not good!")


@task(trigger=any_successful)
def final_task():
    """Convenience final task to do something"""
    print("Cleaning up!")


# ---------------------
# Constructing the flow
# ---------------------
with Flow("Load Process Flow") as flow:

    # Level 1
    dl1_check = check_dl1_stream
    dl2_check = check_dl2_stream
    dl3_check = check_dl3_stream
    dl4_check = check_dl4_stream

    load1 = load_dl1(dl1_check)
    load2 = load_dl2(dl2_check)
    load3 = load_dl3(dl3_check)
    load4 = load_dl4(dl4_check)

    check_1_left = check_level_1_left()
    check_1_left.set_upstream(load1)
    check_1_left.set_upstream(load2)
    check_1_left.set_upstream(load3)
    check_1_left.set_upstream(load4)

    check_1_right = check_level_1_right()
    check_1_right.set_upstream(load1)
    check_1_right.set_upstream(load2)
    check_1_right.set_upstream(load3)
    check_1_right.set_upstream(load4)

    # Level 2
    fl1_check = check_fl1_stream
    fl2_check = check_fl2_stream
    fl3_check = check_fl3_stream
    fl4_check = check_fl4_stream
    fl5_check = check_fl5_stream

    fl1_check.set_upstream(check_1_left)
    fl2_check.set_upstream(check_1_left)
    fl3_check.set_upstream(check_1_left)
    fl4_check.set_upstream(check_1_right)
    fl5_check.set_upstream(check_1_right)

    fload1 = fact_load_1(fl1_check)
    fload2 = fact_load_2(fl2_check)
    fload3 = fact_load_3(fl3_check)
    fload4 = fact_load_4(fl4_check)
    fload5 = fact_load_5(fl5_check)

    check_2_left = check_level_2_left()
    check_2_left.set_upstream(fload1)
    check_2_left.set_upstream(fload2)
    check_2_left.set_upstream(fload3)

    check_2_right = check_level_2_right()
    check_2_right.set_upstream(fload4)
    check_2_right.set_upstream(fload5)

    # Level 3
    af1_check = check_af1_stream
    af2_check = check_af2_stream
    af3_check = check_af3_stream
    af4_check = check_af4_stream

    af1_check.set_upstream(check_2_left)
    af2_check.set_upstream(check_2_left)
    af3_check.set_upstream(check_2_right)
    af4_check.set_upstream(check_2_right)

    afload1 = agg_fact_load_1(af1_check)
    afload2 = agg_fact_load_2(af2_check)
    afload3 = agg_fact_load_3(af3_check)
    afload4 = agg_fact_load_4(af4_check)

    check_success = check_success()
    check_success.set_upstream(afload1)
    check_success.set_upstream(afload2)
    check_success.set_upstream(afload3)
    check_success.set_upstream(afload4)

    check_fail = check_fail()
    check_fail.set_upstream(afload1)
    check_fail.set_upstream(afload2)
    check_fail.set_upstream(afload3)
    check_fail.set_upstream(afload4)

    final_task = final_task()
    final_task.set_upstream(check_success)
    final_task.set_upstream(check_fail)


flow.environment = RemoteEnvironment(executor="prefect.engine.executors.DaskExecutor")
flow.register()
