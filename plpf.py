from datetime import timedelta
import random

from prefect import task, Flow
from prefect.environments import RemoteEnvironment
from prefect.engine.signals import FAIL
from prefect.triggers import any_failed, all_successful, any_successful

# ------------------
# Utility Functions
# ----------------


def _random_failure():
    """Example of a random failure"""
    if random.randint(0, 2) == 1:
        raise FAIL


def _custom_alert_on_failure(obj, old_state, new_state):
    """Example of a custom state handler"""
    if new_state.is_failed():
        print("One of your transactions failed!")
        new_state.message = str(old_state.cached_inputs)
    return new_state


# ------------------
# Extracting Tasks
# ------------------


@task
def get_level_1_data():
    return [1, 2, 3, 4]


@task
def get_level_2_data(partition):
    if partition == "left":
        return [1, 2, 3]
    elif partition == "right":
        return [4, 5]


@task
def get_level_3_data(partition):
    if partition == "left":
        return [1, 2]
    elif partition == "right":
        return [4, 5]


# ------------------
# Loading Tasks
# ------------------


@task(
    max_retries=3,
    retry_delay=timedelta(seconds=5),
    state_handlers=[_custom_alert_on_failure],
)
def load_dimension(d):
    if d == 2:
        raise FAIL
    _random_failure()
    print(f"Your dimension is: {d}")


@task(
    max_retries=3,
    retry_delay=timedelta(seconds=5),
    state_handlers=[_custom_alert_on_failure],
)
def load_fact(d):
    _random_failure()
    print(f"Your fact is: {d}")


@task(
    max_retries=3,
    retry_delay=timedelta(seconds=5),
    state_handlers=[_custom_alert_on_failure],
)
def load_agg_fact(d):
    _random_failure()
    print(f"Your aggregate fact is: {d}")


# ------------------
# Terminal Tasks
# ------------------

# Maybe collect states???
# Halt on failure?
@task(trigger=any_failed)
def exit_log_notify_failure():
    print("One of our crucial tasks failed!")


@task(trigger=all_successful)
def exit_log_notify_success():
    print("This run was very successful!")


@task(trigger=any_successful)
def exit_flow():
    """Purely a convenience task, not necessary, dependent on design"""
    pass


# ------------------
# Flow Definition
# ------------------


with Flow("Prefect Load Process Flow") as flow:
    level_1_data = get_level_1_data()
    load_dimension = load_dimension.map(level_1_data)

    load_fact_1 = load_fact.map(get_level_2_data(partition="left"))
    load_fact_2 = load_fact.map(get_level_2_data(partition="right"))

    load_fact_1.set_upstream(load_dimension)
    load_fact_2.set_upstream(load_dimension)

    load_agg_fact_1 = load_agg_fact.map(get_level_3_data(partition="left"))
    load_agg_fact_2 = load_agg_fact.map(get_level_3_data(partition="right"))

    load_agg_fact_1.set_upstream(load_fact_1)
    load_agg_fact_2.set_upstream(load_fact_2)

    exit_log_notify_failure = exit_log_notify_failure()
    exit_log_notify_failure.set_upstream(load_fact_1)
    exit_log_notify_failure.set_upstream(load_fact_2)
    exit_log_notify_failure.set_upstream(load_agg_fact_1)
    exit_log_notify_failure.set_upstream(load_agg_fact_2)

    exit_log_notify_success = exit_log_notify_success()
    exit_log_notify_success.set_upstream(load_agg_fact_1)
    exit_log_notify_success.set_upstream(load_agg_fact_2)

    exit_flow = exit_flow()
    exit_flow.set_upstream(exit_log_notify_failure)
    exit_flow.set_upstream(exit_log_notify_success)

flow.environment = RemoteEnvironment(executor="prefect.engine.executors.DaskExecutor")
flow.register()
flow.run_agent()
# flow.run()