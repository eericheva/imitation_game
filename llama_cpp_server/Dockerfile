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
ADD llama_cpp_server_config.json .

RUN python -m pip install --no-cache-dir -r requirements.txt

ADD .. /workspace
# Set environment variable for the host
ENV HOST=0.0.0.0
ENV PORT=8080

EXPOSE ${PORT}

ENTRYPOINT [ "python", "-m", "llama_cpp.server", "--config_file", "llama_cpp_server_config.json" ]
#ENTRYPOINT [ "ulimit", "-l", "unlimited", "&&", "python", "-m", "llama_cpp.server", "--config_file", "llama_cpp_server_config.json" ]

# docker build -t llama_cpp_server_image -f ./llama_cpp_server/Dockerfile ./llama_cpp_server
# docker run --name llama_cpp_server_container --network="host" llama_cpp_server_image:latest

# docker build -t ghcr.io/eericheva/llama_cpp_server_image:latest -f Dockerfile ./llama_cpp_server
# docker push ghcr.io/eericheva/llama_cpp_server_image:latest
# docker run --name llama_cpp_server_container --network="host" ghcr.io/eericheva/llama_cpp_server_image:latest

# docker system prune -a
# docker compose up -d
# check if it is ok here : http://<server-ip>
