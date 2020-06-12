
from prefect import Task, Flow
from prefect.tasks.notifications import SlackTask

class GetValue(Task):
    def run(self):
        return "Test SlackTask!"


flow = Flow("slack-test")

value = GetValue()
slack_task = SlackTask()

slack_task.set_upstream(value, key="message", flow=flow)

flow.run()