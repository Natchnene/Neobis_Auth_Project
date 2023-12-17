Auth 
Проект "Auth" представляет собой приложение для регистрации пользователей и аутентификации с использованием jwt.

Характеристики:
- Django, Django Rest Framework
- SqlLite as a project database
- Docker containers

Шаги установки:
- Клонировать этот репозиторий
- Создать файл .env в корне проекта и добавить переменные окружения
    EMAIL_HOST_USER = 'your_email@gmail.com'
    EMAIL_HOST_PASSWORD = 'your_generated_app_password'
    EMAIL_FROM = 'your_email@gmail.com'
- Установите и запустите виртуальное окружение poetry
    - poetry install
    - poetry shell
- Запустите docker
    - docker-compose up

Документация API доступна по следующим ссылкам:

Swagger UI: http://127.0.0.1:8000/swagger/ ReDoc: http://127.0.0.1:8000/redoc/