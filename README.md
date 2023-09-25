# List_recipes
Приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


## Установка и запуск
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/JonyMalikov/List_recipes
```
```
cd List_recipes
```

### Для запуска приложения в контейнерах:
- Установите Docker
- Клонируйте репозиторий
``` git clone git@github.com/JonyMalikov/List_recipes.git ```
- Создайте и заполните файл .env
-- -
### Заполнение .env файла:
- POSTGRES_DB=foodgram
- POSTGRES_USER=foodgram_user
- POSTGRES_PASSWORD=foodgram_password
- DB_NAME=foodgram
- DB_HOST=db
- DB_PORT=5432
- ALLOWED_HOSTS=,127.0.0.1,localhost
- SECRET_KEY=django_secret_key
- DEBUG=True
-- -
- Запустите docker-compose
``` sudo docker-compose up --build ```
- Выполните миграции
``` sudo docker-compose exec backend python3 manage.py migrate ```
- Для сбора статики воспользуйтесь командами
``` sudo docker-compose exec backend python3 manage.py collectstatic ```
``` sudo docker compose exec backend cp -r /app/collected_static/. /static/static/ ``` 
- Для загрузки базы данных ингрединтов
``` sudo docker-compose exec backend management commands python3 manage.py loadcsv ```
- Для создания суперпользователя
``` sudo docker-compose exec backend python3 manage.py createcustomsuperuser ```
-- -

### Сайт доступен по адресу:
https://foodlist.ddns.net
-- -

### Для доступа в админ-зону:
https://foodlist.ddns.net/admin/
- Логин: admin@admin.com
- Пароль: 12345
-- -


## Техническое описание проекта
### Ресурсы 
+ Главная
+ Страница рецепта
+ Страница пользователя
+ Страница подписок
+ Избранное
+ Список покупок
+ Создание и редактирование рецепта


## Используемые технологии
+ Python
+ Django
+ PostgreSQL
+ Docker


## Авторы
+ **Евгений Маликов** [JonyMalikov](https://github.com/JonyMalikov)