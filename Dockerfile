FROM ubuntu:cosmic

 RUN apt-get update && apt-get upgrade -y && \
     add-apt-repository -y ppa:deadsnakes/ppa

 RUN apt-get install python3.7 \
                     python3.7-dev \
                     git \
                     scrot \
                     xsel \
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
                     libtesseract-dev
