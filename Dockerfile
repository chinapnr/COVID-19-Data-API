FROM python:3.6

MAINTAINER David Yi <wingfish@gmail.com>

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

COPY ["./requirements.txt", "."]
RUN pip install -r requirements.txt

COPY ["./app", "/app/covid/app"]
WORKDIR /app/covid/

EXPOSE 8080
ENTRYPOINT ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080","--reload"]