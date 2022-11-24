FROM python:3.7

WORKDIR /scraper

COPY ./requirements.txt .

RUN apt-get update \
    && apt-get install -y \
        build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

COPY ./bulletin/ /scraper/bulletin/

WORKDIR /scraper/bulletin
VOLUME /scraper/out

CMD ["scrapy", "crawl", "bulletin", "-o", "/scraper/out/courses.json"]

