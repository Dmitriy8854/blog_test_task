# blog_test_task
Тестовое задание Блог

## **Инструкция по развертыванию бэкенда в контейнере докер :**

- Клонировать себе репозиторий blog_test_task
- Перейти в папку blog

```cd blog```

- Запустить docker-compose:

```docker compose up --build -d```

- При необходимости выполнить миграции внутри контейнера докер

```
python manage.py makemigrations
python manage.py migrate
```

- Документация redoc и swagger будет доступна по следующим адресам:
```
http://127.0.0.1:8000/api/redoc/
http://127.0.0.1:8000/api/docs/
```