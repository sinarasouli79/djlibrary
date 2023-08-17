FROM python:3.11.4

WORKDIR /app
RUN apt upgrade && apt update
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8000