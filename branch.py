from prefect import Task, Flow


class GetNumber(Task):
    def run(self):
        return 10


class Multiply(Task):
    def run(self, n):
        return n * 10


class Divide(Task):
    def run(self, n):
        return n / 10

class OutputValue(Task):
    def run(self, value):
        print(value)

flow = Flow("branches")

n = GetNumber()

m = Multiply()
d = Divide()

m.set_upstream(n, key="n", flow=flow)
d.set_upstream(n, key="n", flow=flow)

output_1 = OutputValue()
output_2 = OutputValue()

output_1.set_upstream(m, key="value", flow=flow)
output_2.set_upstream(d, key="value", flow=flow)

flow.visualize()
