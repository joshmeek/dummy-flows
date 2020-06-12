from prefect import Task, Flow, task


# @task
# def do_something():
#     print("something")


class DoSomething(Task):
    def run(self):
        return "asdf"


class PrintVal(Task):
    def run(self, val):
        print(val)


do_something = DoSomething()
print_val = PrintVal()

flow = Flow("demo")

print_val.set_upstream(do_something, key="val", flow=flow)

flow.run()
