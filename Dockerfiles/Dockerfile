
FROM prefecthq/prefect:all_extras-0.13.7

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt
ENV A : Guppy

COPY f.prefect f.prefect

RUN python -c "from prefect import Flow; f = Flow.load('/f.prefect'); f.run()"
