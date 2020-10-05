from prefect import task, Flow


@task
def pval(val):
    print(f"My value is {val} and that should be my key ^")


with Flow("mapitems") as flow:
    pval.map(
        ["abc", "def", "ghi"],
        display_name_callable=lambda **kwargs: f"{kwargs['map_index']}-{kwargs['flow_name']}",
    )

flow.run()
# flow.register(project_name="Demo")
