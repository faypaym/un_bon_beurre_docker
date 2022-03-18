#!/usr/bin/python

FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y build-essential

RUN apt-get install -y python3.7
RUN apt install net-tools
RUN apt install nano

COPY ./Client.py /home
