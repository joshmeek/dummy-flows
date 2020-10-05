import random
from prefect import Flow, Task

class ANumber(Task):
    def run(self):
        return random.randint(0, 100)

flow = Flow('Using Operators')
    # a = a_number()
    # b = a_number()

    # add = a + b
    # sub = a - b
    # lt = a < b

a = ANumber()
b = ANumber()

flow.add_task(a)
flow.add_task(b)

add = a.__add__(b)