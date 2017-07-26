FROM python:3.6.2-alpine
ADD . /code
WORKDIR /code
RUN apk add --update linux-headers gcc musl-dev && pip install -r requirements.txt
CMD ["python", "register.py"]
