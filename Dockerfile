# FROM python:3.8-slim-buster

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

# COPY . .

# CMD ["python","manage.py","runserver","0.0.0:8000"]

FROM python:3

ENV PYTHONDONTWRITEBYCODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /code

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt

COPY . /code/
EXPOSE 8003
CMD ["python","manage.py","runserver","0.0.0:8000"]