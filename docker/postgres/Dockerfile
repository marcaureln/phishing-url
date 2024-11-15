FROM postgres:16.4-bullseye

RUN apt-get update \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
