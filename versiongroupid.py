from prefect import Flow, task


@task
def do_nothing():
    print("Nope")


with Flow(
    "version_group_id",
) as flow:
    do_nothing()

flow.register(project_name="QA", version_group_id="asdffdsa")
