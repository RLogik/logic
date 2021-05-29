FROM python:3.10.0b1-slim

################################################################################
# START OF INSTRUCTIONS REQUIRED FOR WHALES PROJECT
# !!! The following lines are necessary for the Whales project !!!
# DEV-NOTE: Add `&& sleep 5` to lines, in order to see the console output.

# NOTE: some default values are sent from .whales scripts via --build-arg flag,
# but user can overwrite these with their own env-values + docker-compose.yml
ARG WHALES_SETUP_PATH
ARG WHALES_PROJECT_NAME
ARG WHALES_SELECTED_SERVICE

## Set whale-labels (used for searching):
LABEL org.whales.project="${WHALES_PROJECT_NAME}"
LABEL org.whales.service="${WHALES_SELECTED_SERVICE}"
LABEL org.whales.initial=true

ARG WD
COPY . "$WD"
WORKDIR "$WD"

# set the Docker-Depth to 1:
RUN echo "1" >| "${WHALES_SETUP_PATH}/DOCKER_DEPTH"
# add prefix to logging levels:
RUN echo "export LOGGINGPREFIX=\">\";" >> "${WHALES_SETUP_PATH}/.lib.globals.sh"

# END OF INSTRUCTIONS REQUIRED FOR WHALES PROJECT
################################################################################

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y dos2unix
RUN apt-get install -y gcc libc-dev
RUN apt-get clean
RUN [ "/bin/bash", "-c", "chmod +x scripts/*.sh" ]
RUN [ "/bin/bash", "-c", "dos2unix scripts/*.sh" ]
