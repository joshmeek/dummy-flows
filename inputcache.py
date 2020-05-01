import datetime
import random

from prefect.engine.cache_validators import all_inputs
from prefect import task, Flow, Parameter

def state_handler(obj, old_state, new_state):
    """
    Any function with this signature can serve as a state handler.

    Args:
        - obj (Union[Task, Flow]): the underlying object to which this state handler
            is attached
        - old_state (State): the previous state of this object
        - new_state (State): the proposed new state of this object

    Returns:
        - Optional[State]: the new state of this object (typically this is just `new_state`)
    """
    print(old_state)
    print(new_state)
    print("CALLLLLLLLEDDDDD @@@@@@@")
    return new_state

@task(cache_for=datetime.timedelta(minutes=5, seconds=30), cache_validator=all_inputs, state_handlers=[state_handler])
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

flow.run(parameters={"x": 4})