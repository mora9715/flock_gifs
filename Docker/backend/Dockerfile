FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt update && apt install libsasl2-dev python-dev libssl-dev -y
RUN pip install --upgrade pip setuptools

WORKDIR /application
COPY ./backend/requirements.txt ./
RUN pip install -r requirements.txt

COPY ./backend ./
RUN python3 manage.py collectstatic

CMD exec gunicorn flock_gifs.wsgi -b 0.0.0.0:8000 -w=1 --threads=16 --max-requests=13000 --max-requests-jitter=1000 --preload --access-logfile=-
