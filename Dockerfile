FROM python:3.9.13-bullseye

ADD . /

RUN apt-get install -y libglib2.0 libnss3 libgconf-2-4 libfontconfig1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
