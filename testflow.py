from prefect import task, Flow, Parameter
from prefect.triggers import any_failed, any_successful


@task
def pull_data():
    return dict(my_key="value")


@task
def get_value(data, key):
    return data[key]


@task(log_stdout=True)
def print_me(val):
    print(val)


@task(trigger=any_failed, log_stdout=True)
def handle_failure():
    print("FAILURE")


@task(trigger=any_successful, log_stdout=True)
def the_end():
    print("We are done.")


with Flow("data-retrieval") as flow:
    key = Parameter("key")
    data = pull_data()
    value = get_value(data=data, key=key)

    printm = print_me

    handlef = handle_failure
    handle_failure.set_upstream(value)

    printm.set_upstream(value, key="val")

    end = the_end
    end.set_upstream(printm)
    end.set_upstream(handlef)

# print(flow.serialize())

flow.register(project_name="Demo")
# flow.visualize()
# flow.run(parameters={"key": "my_key2"})
