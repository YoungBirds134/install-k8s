FROM jupyter/tensorflow-notebook

USER root

RUN sudo apt-get update && apt-get install libsasl2-modules libsasl2-dev

USER $NB_UID

RUN pip3 install pyhive[hive] cassandra-driver

COPY jupyter_notebook_config.json /home/jovyan/.jupyter/

LABEL maintainer="Big Data Demo <haiphucnguyen@gmail.com>"
