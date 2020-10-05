import prefect
from prefect import Flow, Parameter
from prefect.tasks.control_flow.conditional import merge
from prefect.tasks.control_flow.case import case


def main() -> None:
    with Flow("Full inspection") as flow:
        env = Parameter("env", default="DEV", required=False)
        user_token = Parameter("user_token")
        inspection_id = Parameter("inspection_id")
        is_video = Parameter("is_video", default=False, required=False)
        # some tasks
    # Register the flow in Prefect Cloud
    flow.register(project_name="Demo")


if __name__ == "__main__":
    main()