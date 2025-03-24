FROM ubuntu:latest

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y git cmake ninja-build sudo curl wget pkg-config gnupg ca-certificates

COPY keys /root/ranking-languages/keys
RUN gpg --import /root/ranking-languages/keys/*

# C/C++ dependencies 
RUN apt install -y lsb-release wget software-properties-common gnupg
RUN apt-get update

# Clang
ARG CLANG_VERSION=19
RUN curl -sSf https://apt.llvm.org/llvm.sh | bash -s -- ${CLANG_VERSION} all
RUN ln -s /usr/bin/llvm-ar-${CLANG_VERSION} /usr/bin/llvm-ar
RUN ln -s /usr/bin/llvm-profdata-${CLANG_VERSION} /usr/bin/llvm-profdata
RUN ln -s /usr/bin/clang++-${CLANG_VERSION} /usr/bin/clang++

# GCC
ARG GCC_VERSION=13
RUN apt-get install g++-${GCC_VERSION} -y
ENV CC=gcc
ENV CXX=g++

# C/C++ libraries.
RUN apt install -y libapr1-dev libgmp-dev libpcre3-dev libboost-regex-dev libc6-dev libopenblas-dev

# OpenJDK Java
ARG JAVA_VERSION=21.0.4+7
ARG JAVA_CHECKSUM=51fb4d03a4429c39d397d3a03a779077159317616550e4e71624c9843083e7b9
RUN apt install -y libfastutil-java
RUN wget --no-verbose https://github.com/adoptium/temurin21-binaries/releases/download/jdk-${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && echo "${JAVA_CHECKSUM} OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz" | sha256sum --check \
    && tar -C /usr/local --strip-components=1 -xzf OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && rm OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz

# C#.
# https://learn.microsoft.com/en-us/dotnet/core/install/linux-ubuntu-install?tabs=dotnet9&pivots=os-linux-ubuntu-2410
ARG DOTNET_VERSION=8.0
RUN apt install  -y dotnet-sdk-${DOTNET_VERSION}

# Mono
RUN gpg --homedir /tmp --no-default-keyring --keyring /usr/share/keyrings/mono-official-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb [signed-by=/usr/share/keyrings/mono-official-archive-keyring.gpg] https://download.mono-project.com/repo/ubuntu stable-focal main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
RUN apt update
RUN apt install mono-devel -y

# Rust
ARG RUST_VERSION=1.81.0
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y --default-toolchain ${RUST_VERSION}
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustc --version

# Python.
ARG PYTHON_VERSION=3.12
# https://devguide.python.org/getting-started/setup-building/index.html#build-dependencies
# RUN apt install -y build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev libssl-dev
# RUN wget --no-verbose https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
#     && wget --no-verbose https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz.asc \
#     # gpg --verify Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION}.tar.xz \
#     && tar -xJf Python-${PYTHON_VERSION}.tar.xz \
#     && cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations --with-lto && make -j && make install && cd .. \
#     && rm -rf Python-${PYTHON_VERSION}.tar.xz Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION} || cat config.log
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python${PYTHON_VERSION}
RUN apt install python3-pip -y

# PyPy.
RUN add-apt-repository ppa:pypy/ppa
RUN apt update
RUN apt install pypy3 -y

# Script installs
RUN pip3 install rich --break-system-packages

# Nano for debugging
RUN apt install nano

WORKDIR /root/thesis

COPY Benchmarks Benchmarks
COPY Scripts Scripts
COPY RAPL RAPL
COPY Data Data

ENTRYPOINT [ "/bin/bash" ]
