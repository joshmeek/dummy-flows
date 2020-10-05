import copy
from datetime import timedelta
from typing import Union, Dict
import prefect
from prefect.engine import cache_validators
from prefect import task, Flow, Parameter
from prefect.engine.result_handlers import LocalResultHandler


@task(
    result_handler=LocalResultHandler(),
    cache_for=timedelta(seconds=60),
    log_stdout=True,
)
def load_data() -> Dict:
    data = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
    print(data)
    return data


@task(
    result_handler=LocalResultHandler(),
    cache_for=timedelta(seconds=60),
    log_stdout=True,
    # cache_key="testme"
)
def xform_data(data: Dict) -> Dict:
    xformed = copy.deepcopy(data)
    xformed["col_1"] = [v * 2 for v in xformed["col_1"]]
    print(xformed)
    return xformed


@task(log_stdout=True)
def write_data(xformed_data: Dict):
    print(xformed_data)


with Flow("cacheme") as flow:

    raw_data = load_data()
    xformed_value = xform_data(raw_data)
    write_data(xformed_value)

print(flow.register("Demo"))
flow.run_agent(show_flow_logs=True)
