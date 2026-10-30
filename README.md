# Skystore — интернет-магазин на Django

Учебный проект: каталог товаров с категориями, административной панелью, медиафайлами
и наполнением базы через фикстуры и кастомную management-команду.

## Стек

- Python 3.14, Django 6.1
- PostgreSQL 18 (драйвер `psycopg2-binary`)
- Pillow — работа с изображениями товаров
- python-dotenv — чтение настроек из `.env`
- IPython — интерактивный `manage.py shell`

## Структура

```
manage.py
skystore/            # настройки проекта и корневые маршруты
catalog/             # приложение каталога
  models.py          # Category, Product, Contact
  admin.py           # настройки админки
  views.py           # главная страница и контакты
  migrations/        # история миграций
  fixtures/          # categories.json, products.json
  management/commands/load_test_data.py
  templates/         # home.html, contacts.html
screenshots/         # скриншоты работы в shell (задание 5)
.env.sample          # шаблон переменных окружения
```

## Запуск

1. Клонировать репозиторий и перейти в него:

   ```bash
   git clone https://github.com/AlexandrNihsemes/Online-store.git
   cd Online-store
   ```

2. Создать и активировать виртуальное окружение, установить зависимости:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Linux/macOS
   pip install -r requirements.txt
   ```

3. Создать базу данных в PostgreSQL:

   ```sql
   CREATE DATABASE skystore_db WITH ENCODING 'UTF8';
   ```

4. Скопировать `.env.sample` в `.env` и указать свои значения:

   ```
   DB_NAME=skystore_db
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

5. Применить миграции и создать суперпользователя:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Запустить сервер:

   ```bash
   python manage.py runserver
   ```

   Главная — http://127.0.0.1:8000/, контакты — http://127.0.0.1:8000/contacts/,
   админка — http://127.0.0.1:8000/admin/.

## Наполнение базы

Данные хранятся в фикстурах `catalog/fixtures/categories.json` и `products.json`
(UTF-8). Загрузить их по отдельности:

```bash
python manage.py loaddata categories.json
python manage.py loaddata products.json
```

Или одной командой — она сначала очищает таблицы продуктов и категорий,
а затем загружает фикстуры:

```bash
python manage.py load_test_data
```

## Модели

| Модель   | Поля                                                                                                   |
|----------|--------------------------------------------------------------------------------------------------------|
| Category | `name`, `description`                                                                                  |
| Product  | `name`, `description`, `image`, `category` (FK → Category), `price`, `created_at`, `updated_at`        |
| Contact  | `country`, `inn`, `address`, `phone`, `email` — контактные данные на странице `/contacts/`             |

## Работа в shell

Скриншоты сессии лежат в папке [`screenshots/`](screenshots/): создание категорий и продуктов,
выборка всех категорий и продуктов, фильтрация продуктов по категории, обновление цены
и удаление продукта. Рядом с каждым `.png` лежит `.txt` с текстом этой же сессии.
