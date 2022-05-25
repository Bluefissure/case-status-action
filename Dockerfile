FROM python:3.9

# Firefox for Selenium install
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    firefox-esr \
    xvfb \
    && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar zxf geckodriver-v0.30.0-linux64.tar.gz \
    && mv geckodriver /usr/bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]
