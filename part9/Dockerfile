
# -------------------------------------
# first stage
#
FROM python:3.10-slim-bullseye as build

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

# Copy created wheels from build stage
COPY --from=build /usr/src/app/wheels /wheels

# Define environment variables
ENV APP_HOME=/home/app TZ=Europe/Stockholm

# create the app user and update system dependencies
RUN set -eux; \
    addgroup --system app; \
    adduser --system --group app; \
    # Upgrade the package index and install security upgrades \
    apt-get -y update; \
    # Install dependencies \
    pip install --no-cache --upgrade pip; \
    pip install --no-cache /wheels/*; \
    rm -rf /var/lib/apk/lists/*; \
    rm -rf /wheels/*; \
    # Set local timezone (needs to be done before changing user).
    ln -snf /usr/share/zoneinfo/"$TZ" /etc/localtime && echo "$TZ" > /etc/timezone

# set work directory
WORKDIR $APP_HOME

# copy project and chown all the files to the app user
COPY --chown=app:app ./src $APP_HOME/src

# Use argument parameter to build for test, stage or prod environment
ARG BUILD_ENV

# Update gunicorn and uvicorn log level based on master log file configuration and build env.
RUN ["python", "src/config/create_external_config.py"]

# change to the app user
USER app
