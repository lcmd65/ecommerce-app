FROM python:3.10.12-slim as base
WORKDIR /home/app
COPY requirements.txt .

RUN \
    pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /tmp/* && rm -rf /var/tmp/* \
    && rm -rf requirements.txt

RUN \
    apt-get update \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /tmp/* && rm -rf /var/tmp/* \