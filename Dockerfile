FROM python:3

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt
RUN pip install psycopg2

CMD python manage.py runserver 0.0.0.0:8000