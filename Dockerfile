FROM python:3.9.13-bullseye

ADD . /

RUN apt update \
    && apt-get install -y libnss3 chromium

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
