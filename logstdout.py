from prefect import Task, Flow


class MyTask(Task):
    def run(self):
        print("This will be logged!")


flow = Flow("log-stdout")

my_task = MyTask(log_stdout=True)
flow.add_task(my_task)

flow.run()
