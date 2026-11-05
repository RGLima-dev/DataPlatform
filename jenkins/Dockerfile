FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        git \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        python3-pytest \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/dbt-venv \
    && /opt/dbt-venv/bin/pip install --upgrade pip \
    && /opt/dbt-venv/bin/pip install dbt-athena

ENV PATH="/opt/dbt-venv/bin:${PATH}"

RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
        -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        docker-ce-cli \
        docker-compose-plugin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER jenkins