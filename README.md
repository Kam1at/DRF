Домашнее задание №1 по Docker:
Создание контейнера postgres с установленным паролем, именем базы данных, методом подключения по сети и сохранением данных локально на машине:
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test -e POSTGRES_HOST_AUTH_METHOD=md5 -v C:\Users\sdakh\docker\pgdata:/var/lib/postgresql/data postgres

Создание контейнера python с настройкой локальной сети (запуск терминала):
docker run --network host -it python bash

Копирование проекта с локальной машины в контейнер python
docker cp C:\Users\sdakh\PycharmProjects\DRF 03e14d5f7c1f:/home/django

Установка всех необходимых компонентов из файла зависимостей:
pip3 install -r requirements.txt

Также дополнительно установка psycopg2 для работы с базой данных Postgresql:
pip3 install psycopg2
