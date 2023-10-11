# List_recipes
Приложение «Список рецептов»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.


## Установка и запуск
1.
Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/JonyMalikov/List_recipes
```
```
cd List_recipes
```
2.
Для запуска приложения в контейнерах вам понадобится Docker.
Установите Docker, если вы еще не установили его на своей системе.
-- -
3.
Создайте файл .env в корневой папке проекта и заполните его следующим содержимым:
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
4.
- Запустите контейнеры с помощью команды:
``` 
sudo docker-compose up --build
 ```
5.
- Выполните миграции с помощью команды:
```
 sudo docker-compose exec backend python3 manage.py migrate
 ```
6.
- Для сбора статики выполните следующие команды:
```
sudo docker-compose exec backend python3 manage.py collectstatic
```
```
sudo docker compose exec backend cp -r /app/collected_static/. /static/static/
``` 
7.
- Для загрузки базы данных ингредиентов выполните команду:
```
sudo docker-compose exec backend management commands python3 manage.py loadcsv
```
8.
- Для создания суперпользователя выполните команду:
```
sudo docker-compose exec backend python3 manage.py createcustomsuperuser
```
-- -

После завершения этих шагов, ваш сервер будет запущен и ваше приложение будет доступно по адресу
https://127.0.0.1/. Для доступа в админ-зону, используйте следующие учетные данные:
- Логин: admin@admin.com
- Пароль: 12345

Убедитесь, что у вас установлены все зависимости и выполнены все необходимые шаги,
чтобы успешно установить и запустить проект.
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
+ [Python](https://www.python.org/) - язык программирования, на котором написан проект.
+ [Django](https://www.djangoproject.com/) - фреймворк для разработки веб-приложений на языке Python.
+ [Django](https://www.django-rest-framework.org/) Rest Framework - надстройка над Django, облегчающая разработку RESTful API.
+ [PostgreSQL](https://www.postgresql.org/) - реляционная база данных, используемая в проекте.
+ [Docker](https://www.docker.com/) - платформа для контейнеризации и развертывания приложений.


## Авторы
+ **Евгений Маликов** [JonyMalikov](https://github.com/JonyMalikov)