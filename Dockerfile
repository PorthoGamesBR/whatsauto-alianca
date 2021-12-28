FROM python:3.8.10

MAINTAINER 

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./ app

WORKDIR app

ENV FLASK_APP=run.py

ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask","run","--host","0.0.0.0"]
