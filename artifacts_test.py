from prefect import task, Flow, artifacts
from prefect.environments.storage import Local


# @task
# def do_something():
#     mkdown = """
#     # This is markdown

#     [apparently](https://prefect.io)

#     Am I markdown?

#     -----

#     #### We'll find out
#     """

#     artifact_id = artifacts.create_link("https://prefect.io")
#     print(artifact_id)

#     artifacts.update_link(artifact_id, "https://new.co")

#     artifact_id = artifacts.create_markdown(mkdown)
#     print(artifact_id)

# with Flow(
#     "artifacts",
#     storage=Local(
#         stored_as_script=True,
#         path="/Users/josh/Desktop/code/Dummy-Flows/artifacts_test.py",
#     ),
# ) as flow:
#     do_something()

# flow.register("Demo")

import textwrap
from prefect import artifacts, task, Flow


@task(log_stdout=True)
def make_markdown_artifact_no_dedent():
    mkdown = """
    # This is markdown

    [apparently](https://prefect.io)

    Am I markdown?

    -----

    #### We'll find out
    """
    artifact_id = artifacts.create_markdown(mkdown)
    print(artifact_id)


@task(log_stdout=True)
def make_markdown_artifact_dedent():
    mkdown = textwrap.dedent(
        """
    # This is markdown

    [apparently](https://prefect.io)

    Am I markdown?

    -----

    #### We'll find out
    """
    )
    artifact_id = artifacts.create_markdown(mkdown)
    print(artifact_id)

@task(log_stdout=True)
def create_some_links():
    artifact_id_1 = artifacts.create_link("https://prefect.io111")
    print(artifact_id_1)
    artifacts.update_link(artifact_id_1, "https://new.co111")

    artifact_id_2 = artifacts.create_link("https://prefect.io222")
    print(artifact_id_2)
    artifacts.update_link(artifact_id_1, "https://new.co222")

    artifact_id_3 = artifacts.create_link("https://prefect.io333")
    print(artifact_id_3)

    print("Deleting artifact 3")
    artifacts.delete_artifact(artifact_id_2)


with Flow(
    "artifacts",
) as flow:
    no = make_markdown_artifact_no_dedent()
    yes = make_markdown_artifact_dedent()

    links = create_some_links(upstream_tasks=[no, yes])

flow.visualize()