FROM python:3.9.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev gcc wget curl g++ make


RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

RUN mkdir /tas
WORKDIR /tas
COPY entrypoint.sh /tas/
COPY requirements.txt /tas/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /tas/
ENTRYPOINT ["/tas/entrypoint.sh"]

