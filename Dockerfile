FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install psycopg2
RUN pip install uwsgi
RUN pip install -r requirements.txt

EXPOSE 9090
CMD python manage.py boot --settings=modelreg.settings_docker

COPY manage.py /usr/src/app/
COPY modelreg  /usr/src/app/modelreg
