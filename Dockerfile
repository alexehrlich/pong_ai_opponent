FROM python

RUN apt-get update && apt-get install -y python3-pip

RUN pip install pygame

COPY pong.py /app/pong.py

WORKDIR /app

ENTRYPOINT [ "python", "pong.py" ]
