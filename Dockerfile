FROM python:3

ENV CONTAINER_HOME=/var/www
ENV APP_NAME=app


ADD . $CONTAINER_HOME

ENV PYTHONPATH $CONTAINER_HOME/app

WORKDIR $CONTAINER_HOME

RUN pip install -r $CONTAINER_HOME/requirements.txt
