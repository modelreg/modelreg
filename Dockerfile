FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install psycopg2
RUN pip install uwsgi
RUN pip install -r requirements.txt

EXPOSE 9090

ENV DJANGO_SETTINGS_MODULE=modelreg.settings_docker

CMD bash /usr/src/app/boot.sh

COPY scripts/boot.sh /usr/src/app/boot.sh
COPY manage.py /usr/src/app/

COPY modelreg  /usr/src/app/modelreg