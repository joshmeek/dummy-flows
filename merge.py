from prefect.tasks.control_flow import conditional
from prefect import task, Flow

@task
def check():
    print("yes")

with Flow("My Flow") as flow:
    true_branch = True
    false_branch = False
    conditional.ifelse(check, true_branch, false_branch)

    merged_result = conditional.merge(true_branch, false_branch)

flow.run()