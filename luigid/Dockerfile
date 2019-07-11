FROM python:alpine3.9

WORKDIR app
COPY luigi.cfg luigi.cfg

RUN pip install --upgrade pip python-dateutil httplib2 luigi rx sqlalchemy
RUN mkdir /usr/local/luigi

EXPOSE 8082

CMD ["luigid"]
