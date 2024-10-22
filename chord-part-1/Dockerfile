FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3 \
    python3-pip

RUN git clone https://github.com/rpclib/rpclib.git && \
    cd rpclib && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

RUN pip3 install msgpack-rpc-python

CMD ["tail", "-f", "/dev/null"]
