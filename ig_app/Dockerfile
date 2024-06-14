ARG BASE_IMAGE=ubuntu:20.04

FROM ${BASE_IMAGE}

RUN apt update && \
    apt install -y \
        wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
        libreadline-dev libffi-dev libsqlite3-dev libbz2-dev liblzma-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && \
    apt-get install -y tcl

RUN apt-get -y update && \
    apt-get install -y ffmpeg

ARG PYTHON_VERSION=3.11.5

RUN cd /tmp && \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make && make install && \
    cd .. && rm Python-${PYTHON_VERSION}.tgz && rm -r Python-${PYTHON_VERSION} && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip && \
    python -m pip install --upgrade pip && \
    rm -r /root/.cache/pip

WORKDIR /workspace

ADD requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

ADD .. /workspace
CMD ["python", "main.py"]

# docker build -t imitation_game_image -f Dockerfile ./ig_app
# docker run --name imitation_game_container --network="host" imitation_game_image:latest

# docker build -t ghcr.io/eericheva/imitation_game_image:latest -f Dockerfile ./ig_app
# docker push ghcr.io/eericheva/imitation_game_image:latest
# docker run --name imitation_game_container --network="host" ghcr.io/eericheva/imitation_game_image:latest

# docker system prune -a
# docker compose up -d
# check if it is ok here : http://<server-ip>
