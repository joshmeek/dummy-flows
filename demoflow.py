from prefect import task, Flow


@task
def getval():
    return "HERE"

@task
def printme(x):
    print(x)

with Flow("test-flow") as flow:
    val = getval()
    printme(val)

flow.run()