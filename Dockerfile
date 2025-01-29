FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    python3-pip

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -U pip && \
    pip install -r /app/requirements.txt 

COPY ./src /app/src

WORKDIR /app/src

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
