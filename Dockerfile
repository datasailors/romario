FROM tensorflow/tensorflow:1.13.1-py3

MAINTAINER Fabio Nonato <https://github.com/fabiononato>

ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG KFP_PACKAGE

ADD Container-Root /

RUN export http_proxy=$http_proxy; export https_proxy=$https_proxy; export no_proxy=$no_proxy; /setup.sh; rm -f /setup.sh

RUN pip install -U \
    -r requirements.txt

# Installing Kubeflow from repo - KFP_PACKAGE passed as build argument.
RUN pip install $KFP_PACKAGE --upgrade --no-cache

WORKDIR /

# CMD /startup.sh

CMD python /service/romario.py
