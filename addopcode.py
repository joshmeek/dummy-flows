from prefect import Flow, Task

class AddTask(Task):

    def __init__(self, default: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default= default

    def run(self, x: int, y: int=None) -> int:
        if y is None:
            y = self.default
        print(x + y)
        return x + y

add = AddTask(default=1)

with Flow("oppcode?") as f:
    first_result = add(1, y=2)
    second_result = add(x=first_result, y=100)

f.register("Demo")