
# -------------------------------------
# first stage
#
FROM python:3.10-slim-bullseye as build1

# set work directory
WORKDIR /usr/src/app

# Use argument parameter to build for test, stage or prod environment
ARG BUILD_ENV

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# don't generate byte code
ENV PYTHONDONTWRITEBYTECODE=1

# install system dependencies
RUN apt-get -y update

# install python dependencies
RUN pip install --upgrade pip setuptools wheel
COPY requirements_${BUILD_ENV}.txt ./requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# -------------------------------------
# second stage
#
FROM python:3.10-slim-bullseye

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV APP_HOME=/home/app
RUN mkdir -p $APP_HOME

# set work directory
WORKDIR $APP_HOME

# Use argument parameter to build for test, stage or prod environment
ARG BUILD_ENV

# install system dependencies
RUN apt-get -y update

# Set local timezone (needs to be done befor changing user).
ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python dependencies
COPY --from=build1 /usr/src/app/wheels /wheels
RUN pip install --no-cache --upgrade pip \
    && pip install --no-cache /wheels/*

# copy project and chown all the files to the app user
COPY --chown=app:app part9/src $APP_HOME/src
COPY --chown=app:app logging_config_${BUILD_ENV}.json $APP_HOME/logging_config.json

# Update gunicorn and uvicorn log level based on master log file configuration and build env.
RUN ["python", "src/config/create_external_config.py", "logging_config.json"]

# change to the app user
USER app
