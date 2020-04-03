FROM python:3.7

MAINTAINER David Yi <wingfish@gmail.com>

COPY ["./requirements.txt", "."]
RUN pip install -r requirements.txt

COPY ["./app", "/app/covid/app"]
WORKDIR /app/covid/

EXPOSE 8080
ENTRYPOINT ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080","--reload"]