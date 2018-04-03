FROM python:3.5-alpine
MAINTAINER Helen <le0nana0888@gmail.com>

ENV INSTALL_PATH /mls
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "mls.app:create_app()"