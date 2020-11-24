import prefect
from prefect import task, Flow


@task(log_stdout=True)
def check():
    print(prefect.context.get("flow_id"))
    print(prefect.context.get("TEST"))
    print(prefect.context.get("logging", {}).get("level"))


f = Flow(
    "ctx-check",
    tasks=[check],
    storage=prefect.environments.storage.Local(
        stored_as_script=True, path="/Users/josh/Desktop/code/Dummy-Flows/ctx_check.py"
    ),
)

f.register("Demo")