from prefect import task, Flow

@task(log_stdout=True)
def task_1():
    print("In task1")
    #create some files
    return 1

@task(log_stdout=True)
def task_2(val_1):
    print("In task2")
    print("val1: {}".format(val_1))
    return 2

@task(log_stdout=True)
def task_3(val_1, val_2):
    print("In task3")
    print("val1: {}, val_2:{}".format(val_1, val_2))
    return 3

with Flow("Seq_flow_with_args") as flow:

    # I need to store the result of task_1 here
    # to send to task_2 & task_3 later

    t1 = task_1()
    t2 = task_2(t1)
    t3 = task_3(t1, t2)


    # # I need to store the result of task2 here
    # flow.set_dependencies(
    #     task=task_2(result_of_task1),
    #     upstream_tasks=[task_1])  # since task_2 will read the files generated by task_1


    # # I need to send task3 2 results: result_of_task1, result_of_task1
    # flow.set_dependencies(
    #     task=task_3(result_of_task1, result_of_task2),
    #     upstream_tasks=[task_2])

flow.run()