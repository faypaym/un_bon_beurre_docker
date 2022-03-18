#!/usr/bin/python

FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y build-essential

RUN apt-get install -y python3
RUN apt install net-tools
RUN apt install nano


#COPY ./requirements.txt ./


#RUN apt install libmariadb3 libmariadb-dev
RUN apt install python3-pip -y
RUN pip3 install mysql-connector-python

COPY ./Server.py /home

