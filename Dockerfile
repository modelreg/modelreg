FROM python:3
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --settings=modelreg.settings_docker

EXPOSE 8080

CMD python manage.py boot --settings=modelreg.settings_docker
