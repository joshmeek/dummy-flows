from prefect import Task, Flow

class TaskA(Task):
    def run(self):
        print("Starting A")
        records = [
            {"data": "dummy"},
            {"data": "dummier"},
            {"data": "dummiest"},
        ]
        return records


class TaskB(Task):
    def run(self):
        print("Starting B")
        print("doing something unrelated")


class TaskC(Task):
    def run(self, data):
        print("Starting C")
        # raise RuntimeError("Uncomment this to fix")
        print(f"Data: {data}")


class TaskD(Task):
    def run(self, data):
        print("Starting D")
        print("Cleaning up failure")
        print(data)

task_a = TaskA()
task_b = TaskB()
task_c = TaskC()
task_d = TaskD()

with Flow("test") as f:
    task_c.set_upstream(task_a, key="data", mapped=True)
    task_c.set_upstream(task_b)

    task_d.set_upstream(task_a, key="data", mapped=True)
    task_d.set_upstream(task_c)

# f.visualize()
f.run()