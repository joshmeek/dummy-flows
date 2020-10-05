from prefect import Task, Flow
from prefect.tasks.shell import ShellTask

class ShowOutput(Task):
    def run(self, std_out):
        print(std_out)

ls_task = ShellTask(command="ls", return_all=True)
show_output = ShowOutput()

ls_count = ShellTask(command="ls | wc -l", return_all=True)
show_output2 = ShowOutput()

flow = Flow("list_files")
show_output.set_upstream(ls_task, key="std_out", flow=flow)
show_output2.set_upstream(ls_count, key="std_out", flow=flow)

flow.run()