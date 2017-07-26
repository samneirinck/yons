FROM python:3.6.2-alpine
ADD . /code
WORKDIR /code
RUN apk add --update --no-cache g++ gcc libxslt-dev && pip install -r requirements.txt
CMD ["python", "musicservice.py"]
