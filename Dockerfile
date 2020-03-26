FROM python:3

#Force the stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED 1

WORKDIR /app/src

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

COPY manage.py /app/src/
