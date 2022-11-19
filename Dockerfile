FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
# RUN add-apt-repository universe
# RUN apt-get update
# RUN apt-get install -y python3-pip
# RUN apt-get install python3-dev default-libmysqlclient-dev build-essential
RUN pip3 install -r requirements.txt
COPY . /app
