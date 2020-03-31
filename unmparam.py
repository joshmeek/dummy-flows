# with Flow(pathlib.Path(__file__).stem, SCHEDULE, HANDLER) as flow:
#     profiles = generate_profiles()
#     environment = Parameter('environment', default=None) # options: acquisition_public, reports_public
#     timestamp_column = Parameter('timestamp_column', default=None)
#     test_type = Parameter('test_type', default=None) # options: out_of_sync_missing, out_of_sync_jsonb
#     env_config = setup(environment, test_type)
#     snowflake_setup = create_snowflake_objects(env_config)
#     tables = fetch_table_info_for_tests(env_config, timestamp_column, test_type)
#     test_suite = create_test.map(tables, unmapped(env_config), unmapped(test_type))
#     dbt_operations = dbt_task(command='dbt run-operation create_udfs')
#     test_command = test_command_task(tag=test_type)
#     dbt_test = dbt_task(command=test_command)
#     successful_run = update_state()
#     failed_run = analyze_failures()
#     dbt_operations.set_upstream(snowflake_setup)
#     dbt_operations.set_upstream(test_suite)
#     dbt_operations.set_upstream(profiles)
#     dbt_test.set_upstream(dbt_operations)
#     failed_run.set_upstream(dbt_test)
#     successful_run.set_upstream(dbt_test)
#     flow.set_reference_tasks([dbt_test])

from prefect import task, Flow, Parameter, unmapped
from prefect.environments import RemoteEnvironment


@task
def vals():
    return [1, 2, 3]


@task
def mult(val, p):
    print(val * p)


with Flow(
    "unmapped-params",
    environment=RemoteEnvironment(executor="prefect.engine.executors.DaskExecutor"),
) as flow:
    p = Parameter("p", default=None)
    vals = vals()
    mult.map(vals, unmapped(p))

# print(flow.schedule)
flow.register(project_name="QA")
# flow.run(parameters=dict(p=2))
