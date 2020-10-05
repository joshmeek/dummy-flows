from prefect import task, Flow

@task(tags=["LIMIT"])
def a():
    print("AAAA")
    return "AAAA"

f = Flow('limit-reached', tasks=[a])

f.register(project_name="Demo")