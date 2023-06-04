from ubuntu:22.04

RUN apt update
RUN apt install software-properties-common -y

RUN mkdir -p /var/log
RUN mkdir -p /etc/certs
RUN mkdir -p /usr/local/bin

COPY db_conf.json /etc/db_conf.json
COPY nginx-ca.crt /etc/certs/nginx-ca.crt
COPY nginx-ca.key /etc/certs/nginx-ca.key
COPY audiobook_converter /usr/local/bin/audiobook_converter

CMD ["/usr/local/bin/audiobook_converter"]
