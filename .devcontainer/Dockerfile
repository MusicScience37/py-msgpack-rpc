FROM musicscience37/pipenv:jammy

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-client \
    gnupg2 \
    vim nano \
    && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    rm -r /var/lib/apt/lists/*
