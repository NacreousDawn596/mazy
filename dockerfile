FROM python:3.11.6
LABEL Maintainer="NacreousDawn596@pm.me"

WORKDIR /opt/app

COPY ./requirements.txt /opt/app

RUN pip install -r /opt/app/requirements.txt

COPY . /opt/app

CMD [ "python", "./main.py" ]