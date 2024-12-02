FROM ubuntu:latest

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y git cmake ninja-build sudo curl wget pkg-config gnupg

COPY keys /root/ranking-languages/keys
RUN gpg --import /root/ranking-languages/keys/*

# C++
# ARG CLANG_VERSION=19
# RUN apt install -y lsb-release wget software-properties-common gnupg
# RUN curl -sSf https://apt.llvm.org/llvm.sh | bash -s -- ${CLANG_VERSION} all
# ENV CC=clang-${CLANG_VERSION}
# ENV CXX=clang++-${CLANG_VERSION}
# RUN ln -s /usr/bin/llvm-ar-${CLANG_VERSION} /usr/bin/llvm-ar
# RUN ln -s /usr/bin/llvm-profdata-${CLANG_VERSION} /usr/bin/llvm-profdata

ARG GCC_VERSION=
RUN apt install -y lsb-release wget software-properties-common gnupg
RUN apt-get update
RUN apt-get install g++ -y
ENV CC=gcc
ENV CXX=g++



# C/C++ libraries.
RUN apt install -y libapr1-dev libgmp-dev libpcre3-dev libboost-regex-dev libc6-dev


# Rust
ARG RUST_VERSION=1.81.0
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y --default-toolchain ${RUST_VERSION}
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustc --version

# Python.
# TODO specific version
RUN apt install python3 python3-pip -y
# ARG PYTHON_VERSION=3.12.6
# # https://devguide.python.org/getting-started/setup-building/index.html#build-dependencies
# RUN apt install -y build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev libssl-dev
# RUN wget --no-verbose https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
#     && wget --no-verbose https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz.asc \
#     # gpg --verify Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION}.tar.xz \
#     && tar -xJf Python-${PYTHON_VERSION}.tar.xz \
#     && cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations --with-lto && make -j && make install && cd .. \
#     && rm -rf Python-${PYTHON_VERSION}.tar.xz Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION} || cat config.log

# Script installs
RUN pip3 install rich --break-system-packages

# C#.
# https://dotnet.microsoft.com/en-us/download/dotnet
ARG DOTNET_VERSION=8.0.401 # 8.0.8.
ARG DOTNET_URL=https://download.visualstudio.microsoft.com/download/pr/db901b0a-3144-4d07-b8ab-6e7a43e7a791/4d9d1b39b879ad969c6c0ceb6d052381/dotnet-sdk-8.0.401-linux-x64.tar.gz
ARG DOTNET_CHECKSUM=4d2180e82c963318863476cf61c035bd3d82165e7b70751ba231225b5575df24d30c0789d5748c3a379e1e6896b57e59286218cacd440ffb0075c9355094fd8c
RUN wget --no-verbose ${DOTNET_URL} \
    && echo "${DOTNET_CHECKSUM} dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz" | sha512sum --check \
    && tar -C /usr/local/bin -xzf dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz \
    && rm dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz


# Java.
ARG JAVA_VERSION=21.0.4+7
ARG JAVA_CHECKSUM=51fb4d03a4429c39d397d3a03a779077159317616550e4e71624c9843083e7b9
RUN apt install -y libfastutil-java
RUN wget --no-verbose https://github.com/adoptium/temurin21-binaries/releases/download/jdk-${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && echo "${JAVA_CHECKSUM} OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz" | sha256sum --check \
    && tar -C /usr/local --strip-components=1 -xzf OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && rm OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz


WORKDIR /root/ranking-languages
COPY Benchmarks Benchmarks
COPY Data Data
COPY Scripts Scripts
COPY Results Results
COPY RAPL RAPL
ENTRYPOINT [ "/bin/bash" ]
# ENTRYPOINT [ "python3", "-m", "Scripts.measure" ]
