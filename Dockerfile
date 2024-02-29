FROM python

RUN apt install pygame

ENTRYPOINT [ "python", "pong.py" ]