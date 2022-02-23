FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./app /app
COPY ./alembic.ini /alembic.ini
COPY ./.env /.env
COPY ./config.cfg /config.cfg

EXPOSE 80:80
EXPOSE 5191:5191