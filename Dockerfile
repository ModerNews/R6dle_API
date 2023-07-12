FROM python:3.11-alpine

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY app /app/app
COPY static /app/static

WORKDIR /app/app

ENTRYPOINT ["uvicorn", "factory:app", "--reload", "--host", "0.0.0.0"]