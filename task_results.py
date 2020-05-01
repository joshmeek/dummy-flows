from prefect import Task, Flow

class GetValue(Task):
    def run(self):
        return 10

class AddValue(Task):
    def run(self, v):
        return v + 10

class PrintValue(Task):
    def run(self, v):
        print(v)

# with Flow("task-results") as flow:
#     v = get_value()
#     v_added = add_value(v)
#     p = print_value(v_added)

flow = Flow("task-results")

get_value = GetValue()
add_value = AddValue()
print_value = PrintValue()

get_value.set_downstream(add_value, key="v", flow=flow)
add_value.set_downstream(print_value, key="v", flow=flow)

state = flow.run()

assert state.result[get_value].result == 10
assert state.result[add_value].result == 20
assert state.result[print_value].result == None