FROM ubuntu:xenial
MAINTAINER Kimberly Sereduck <ksereduck@mozilla.com>
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install software-properties-common -y && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && apt-get install \
    python3.7 \
    python3.7-dev \
    git \
    scrot \
    xsel \
    p7zip-full \
    libopencv-dev \
    autoconf automake libtool \
    autoconf-archive \
    pkg-config \
    libpng-dev \
    libjpeg8-dev \
    libtiff5-dev \
    zlib1g-dev \
    libicu-dev \
    libpango1.0-dev \
    libcairo2-dev \
    firefox \
    wmctrl \
    xdotool \
    python3.7-tk \
    tesseract-ocr \
    zip \
    unzip \
    python3-pip \
    wget \
    libtesseract-dev \
    xvfb \
    x11-apps -y

WORKDIR /bin

RUN wget http://www.leptonica.org/source/leptonica-1.76.0.tar.gz && \
    tar xopf leptonica-1.76.0.tar.gz && cd leptonica-1.76.0 && \
    ./configure && make && make install

RUN wget https://github.com/tesseract-ocr/tessdata/archive/4.0.0.zip && \
    unzip 4.0.0.zip && cd tessdata-4.0.0 && \
    mkdir /usr/local/share/tessdata/ && \
    mv * /usr/local/share/tessdata/

RUN apt-get install gdb -y
RUN python3.7 -m pip install -U pip setuptools
COPY ./requirements.txt /iris/requirements.txt
WORKDIR /iris
RUN python3.7 -m pip install -r /iris/requirements.txt
COPY . /iris
RUN pip install .

ENV DISPLAY :99.0
ENV -x +e -v
ENV XAUTH $HOME/.Xauthority
RUN touch $XAUTH
ENV IRIS_CODE_ROOT /iris
ENV PYTHONPATH /iris
RUN Xvfb :99 -screen 0 1920x1080x24+32 +extension GLX +extension RANDR &> xvfb.log && \
    iris sample -n -i DEBUG
