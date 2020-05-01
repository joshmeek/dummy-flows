from random import random

from prefect import Task, Flow
from prefect.tasks.control_flow.conditional import CompareValue, Merge


class CheckCondition(Task):
    def run(self):
        return random() < 0.5


class AsBool(Task):
    def run(self, x):
        return bool(x)


class ActionIfTrue(Task):
    def run(self):
        print("I am true!")


class ActionIfFalse(Task):
    def run(self):
        print("I am false!")


flow = Flow("conditional-branches")

check_condition = CheckCondition()

as_bool = AsBool()

as_bool.set_upstream(check_condition, key="x", flow=flow)


compare_true = CompareValue(True)
compare_false = CompareValue(False)

compare_true.set_upstream(as_bool, key="value", flow=flow)
compare_false.set_upstream(as_bool, key="value", flow=flow)

true_branch = ActionIfTrue()
false_branch = ActionIfFalse()

true_branch.set_upstream(compare_true, flow=flow)
false_branch.set_upstream(compare_false, flow=flow)

merge = Merge()
merge.set_upstream(true_branch, key="task1", flow=flow)
merge.set_upstream(false_branch, key="task2", flow=flow)

flow.run()
