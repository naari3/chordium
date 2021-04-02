FROM python:3.8 AS builder

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --system


FROM python:3.8 AS fluid-builder

RUN apt-get update && apt-get install -y cmake \
  && git clone https://github.com/FluidSynth/fluidsynth.git \
  && cd fluidsynth \
  && git checkout tags/v2.1.8 \
  && mkdir build && cd build \
  && cmake .. && make install \
  && mv /usr/local/lib64/libfluidsynth.so* /usr/local/lib \
  && tar czf libfluidsynth.tar.gz /usr/local/lib/libfluidsynth.so* \
  && tar czf libgthread.tar.gz /usr/lib/x86_64-linux-gnu/libgthread-2.0.so* \
  && tar czf libglib.tar.gz /usr/lib/x86_64-linux-gnu/libglib-2.0.so* \
  && tar czf libgomp.tar.gz /usr/lib/x86_64-linux-gnu/libgomp.so*


FROM python:3.8 AS ffmpeg-builder

RUN apt-get update && apt-get install -y xz-utils curl \
  && curl -sO https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz \
  && tar xJf ffmpeg-git-amd64-static.tar.xz \
  && mv ffmpeg-git-*-amd64-static/ffmpeg /usr/local/bin/


FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY --from=ffmpeg-builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg

COPY --from=fluid-builder /fluidsynth/build/libfluidsynth.tar.gz /libfluidsynth.tar.gz
COPY --from=fluid-builder /fluidsynth/build/libgthread.tar.gz /libgthread.tar.gz
COPY --from=fluid-builder /fluidsynth/build/libglib.tar.gz /libglib.tar.gz
COPY --from=fluid-builder /fluidsynth/build/libgomp.tar.gz /libgomp.tar.gz
RUN cd / \
  && tar xzf libfluidsynth.tar.gz \
  && tar xzf libgthread.tar.gz \
  && tar xzf libglib.tar.gz \
  && tar xzf libgomp.tar.gz \
  && ldconfig

WORKDIR /app

COPY . ./

CMD ["python", "main.py"]

