FROM python:3.6.4-slim-stretch

RUN mkdir /app
WORKDIR /app

RUN mkdir /db

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
COPY run_aquabot.py /app

#Commented out on server version (may need to comment out again)
COPY ./aquabot/db/. /db

ENV DATABASE_PATH /db
ENV FLASK_APP run_aquabot.py

EXPOSE 5000
CMD flask run --host=0.0.0.0