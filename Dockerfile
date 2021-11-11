FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./docker-entrypoint.sh /
COPY requirements.txt /code/
RUN pip install -r requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]