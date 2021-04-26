FROM ubuntu:18.04

RUN apt update
RUN apt install python3 python3-pip libmysqlclient-dev git -y
RUN pip3 install flask flask-mysqldb
COPY . .
EXPOSE 3000

CMD ["python3", "App.py"]
