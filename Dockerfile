FROM python:3.10.5-bullseye

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./eng_django /app

WORKDIR /app

COPY ./entrypoint.sh /
EXPOSE 8000 8100
ENTRYPOINT ["sh", "/entrypoint.sh"]