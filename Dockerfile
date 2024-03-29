FROM python:3.9

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install six
RUN pip install -r requirements.txt