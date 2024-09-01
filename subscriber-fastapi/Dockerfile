FROM ubuntu:latest

WORKDIR /app

COPY .  .

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN pip3 install -r ./requirements.txt --break-system-packages

EXPOSE 8000

CMD [ "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000" ]