from random import sample

from prefect import Flow, Parameter, Task, unmapped


class GetNumbers(Task):
    def run(self, total):
        return sample(range(100), total)


class OutputValue(Task):
    def run(self, n, multiple):
        print(n * multiple)


flow = Flow("unmapped-values")

total = Parameter("total")
multiple = Parameter("multiple")

numbers = GetNumbers()
numbers.set_upstream(total, key="total", flow=flow)

output_value = OutputValue()
output_value.bind(mapped=True, n=numbers, multiple=unmapped(multiple), flow=flow)

# with Flow("unmapped-values") as flow:
#     total = Parameter("total")
#     multiple = Parameter("multiple")

#     numbers = get_numbers(total)

#     output_value.map(numbers, multiple=unmapped(multiple))

flow.run(parameters={"total": 5, "multiple": 10})
