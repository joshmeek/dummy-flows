from random import randrange

from prefect import Flow, Parameter, Task

# from prefect.tasks.core import
from prefect.engine.executors import DaskExecutor


class RandomNum(Task):
    def run(self, stop):
        number = randrange(stop)
        print(f"Your number is {number}")
        return number


class Sum(Task):
    def run(self, numbers):
        print(sum(numbers))


flow = Flow("parallel-execution")

stop = Parameter("stop")

number_1 = RandomNum()
number_2 = RandomNum()
number_3 = RandomNum()

stop.set_downstream(number_1, key="stop", flow=flow)
stop.set_downstream(number_2, key="stop", flow=flow)
stop.set_downstream(number_3, key="stop", flow=flow)

sum_numbers = Sum()

sum_numbers.bind(numbers=[number_1, number_2, number_3], flow=flow)
# with Flow("parallel-execution") as flow:
#     stop = Parameter("stop")

#     number_1 = random_num(stop)
#     number_2 = random_num(stop)
#     number_3 = random_num(stop)

#     sum = sum(numbers=[number_1, number_2, number_3])

# flow.visualize()
flow.run(parameters={"stop": 5}, executor=DaskExecutor())
