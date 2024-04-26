# referral-system

Простая реферальная система с минимальным интерфейсом.

## Стек

- Python
- Django
- DRF
- Simple JWT
- drf-spectacular
- PostgreSQL

## Запуск проекта

Клонируйте репозиторий:

```bash
git clone git@github.com:galirkil/referral-system.git
```

Перейдите в папку с проектом, установите и активируйте виртуальное окружение:

```bash
cd referral-system
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте и заполните файл `.env` в корневой папке проекта по шаблону:

```env
SECRET_KEY=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
HOST=
PORT=
```

Выполните миграции:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Создайте суперпользователя:

```bash
python3 manage.py createsuperuser
```

Запустите сервер:

```bash
python3 manage.py runserver
```

## Запуск тестов

```bash
python3 manage.py test
```

## Документация API

Документация API приложения доступна по
ссылке - http://localhost:8000/api/schema/redoc/