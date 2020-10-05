from prefect import task, Flow

@task
def help():
    print("me")

with Flow("help me flow") as flow:
    h = help()

flow.run()