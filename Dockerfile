FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirement.txt /usr/src/app/
RUN mkdir /usr/src/app/templates
COPY templates/ /usr/src/app/templates
COPY app.py /usr/src/app/
COPY zozo.py /usr/src/app/

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]
