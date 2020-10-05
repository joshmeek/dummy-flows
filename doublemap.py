from prefect import task, Flow, Parameter, unmapped


@task
def do_something(a, b):
    print(a)
    print(b)


with Flow("two-map") as flow:
    a = Parameter("a")
    b = Parameter("b")

    do_something.set_upstream(a, key="a", mapped=True)
    do_something.set_upstream(b, key="b", mapped=True)

# flow.run(parameters={"a": [1, 2, 3], "b": [4, 5, 6]})


@task
def backfill_task_result(symbol, backfill_date, tick_type):
    print(symbol)
    print(backfill_date)
    print(tick_type)


with Flow("backfill-map") as flow:
    backfill_task_result.map(
        symbol=["SPY", "GLUU", "IHI", "NVDA"],
        backfill_date=["2020-07-01", "2020-07-02"],
        tick_type=unmapped("trades"),
    )

# flow.run()


@task
def get_symbols():
    return ["SPY", "GLUU", "IHI", "NVDA"]

@task
def apply_dates(symbols, date):
    return [[symbol, date] for symbol in symbols]

@task
def backfill_task_result(symbol_date, tick_type):
    print(symbol_date)
    print(tick_type)

with Flow("backfill-map") as flow:
    symbol_date = apply_dates.map(symbols=unmapped(['SPY','GLUU','IHI','NVDA']), date=['2020-07-01','2020-07-02'])
    backfill_task_result.map(symbol_date=symbol_date, tick_type=unmapped('trades'))

flow.run()