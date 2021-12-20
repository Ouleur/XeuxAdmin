FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano python3-dev \
    musl-dev \
    postgresql-dev \
    gcc \
    && pip install --no-cache-dir psycopg2 \
    && apk del --no-cache .build-deps

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
ENV MAIL_USERNAME ouleur000@gmail.com
ENV MAIL_PASSWORD 01709902#ouleur
ENV DEV_DATABASE_URL postgresql:///one4driver_dev
ENV TEST_DATABASE_URL postgresql:///one4driver_test
ENV DATABASE_URL postgresql:///one4driver_prod
ENV POSTGRES_URL 172.17.0.3:5432
ENV POSTGRES_USER postgres
ENV POSTGRES_PW odoo
ENV POSTGRES_DB odoo

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /var/www/requirements.txt
