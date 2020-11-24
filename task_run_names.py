
from prefect import task, Flow

@task
def get_values():
    return ["value", "test", "demo"]

@task(task_run_name=lambda **kwargs: f"{kwargs['val']}")
def compute(val):
    if val == "demo":
        raise ValueError("Nope!")

with Flow("task_run_names") as flow:
    vals = get_values()
    compute.map(vals)

flow.run()
# flow.register(project_name="Demo")

# from prefect import Task, Flow

# class GetValues(Task):
#     def run(self):
#         return ["value", "test", "demo"]

# class Compute(Task):
#     def run(self, val):
#         if val == "demo":
#             raise ValueError("Nope!")

# flow = Flow("task_run_names")

# vals = GetValues()
# compute = Compute(task_run_name=lambda **kwargs: f"{kwargs['val']}")

# compute.set_upstream(vals, flow=flow, key="val", mapped=True)

# flow.run()