FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install apt-utils python3 -y python3-pip -y

RUN mkdir -p /root/.pip

ADD pip.conf /root/.pip/

COPY nsfw /root/nsfw

RUN cd /root/nsfw && pip3 install -r requirements.txt

CMD ["/usr/bin/python3", "/root/nsfw/api.py"]
