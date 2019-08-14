FROM python:3.7

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install numpy

WORKDIR /
ENV OPENCV_VERSION="4.1.0"
RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
&& unzip ${OPENCV_VERSION}.zip \
&& mkdir /opencv-${OPENCV_VERSION}/cmake_binary \
&& cd /opencv-${OPENCV_VERSION}/cmake_binary \
&& cmake -DBUILD_TIFF=ON \
  -DBUILD_opencv_java=OFF \
  -DWITH_CUDA=OFF \
  -DWITH_OPENGL=ON \
  -DWITH_OPENCL=ON \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DCMAKE_INSTALL_PREFIX=$(python3.7 -c "import sys; print(sys.prefix)") \
  -DPYTHON_EXECUTABLE=$(which python3.7) \
  -DPYTHON_INCLUDE_DIR=$(python3.7 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python3.7 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
  .. \
&& make install \
&& rm /${OPENCV_VERSION}.zip \
&& rm -r /opencv-${OPENCV_VERSION}

RUN apt-get update && apt-get install -y libgif7
RUN apt-get install -y python-psycopg2

RUN apt-get update && apt-get install -y apt-transport-https

RUN echo 'deb https://notesalexp.org/debian/stretch/ stretch main' > /etc/apt/sources.list
RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add -
RUN apt-get update

RUN apt-get update && apt-get install -y libtesseract4 liblept5
RUN apt-get update && apt-get install -y tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr-rus

RUN apt-get update && apt-get install -y libtesseract-dev libleptonica-dev

# TODO: Move to requirements.txt
RUN pip install youtube_dl
RUN pip install sqlalchemy
RUN pip install psycopg2
RUN pip install git+https://github.com/sirfz/tesserocr.git
RUN pip install git+https://github.com/mps-youtube/pafy.git
RUN pip install flask
RUN pip install flask-sqlalchemy
RUN pip install flask-migrate
RUN pip install gunicorn
RUN pip install rq
RUN pip install pillow
RUN pip install Flask-HTTPAuth

RUN ln -s \
  /usr/local/python/cv2/python-3.7/cv2.cpython-37m-x86_64-linux-gnu.so \
  /usr/local/lib/python3.7/site-packages/cv2.so

ADD . /app
WORKDIR /app

RUN chmod u+x ./entrypoint.sh

ENV DATABASE_URL="postgresql://postgres@db:5432/arthas_networth"
ENV REDIS_URL="redis://redis:6379"
