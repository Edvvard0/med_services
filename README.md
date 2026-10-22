<div align="center">

# 🏥 med_services

**Медицинская информационная система (МИС): пациенты, госпитализации и направления на процедуры**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-default-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-async-D71F00?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

## 📖 О проекте

Первая версия МИС: веб-интерфейс и REST API для управления потоком пациентов клиники — регистрация, госпитализация и направление на лечебно-диагностические мероприятия. Пациенты и врачи авторизуются раздельно.

> Продолжение разработки (PostgreSQL, миграции, учёт коек, Docker Compose) — в репозитории [med_system](https://github.com/Edvvard0/med_system).

## ✨ Возможности

- **Регистрация пациентов** — ФИО, паспорт, страховой полис; UUID медкарты; фото; QR-код медкарты
- **Документы** — договор на обслуживание и согласие на обработку данных в `.docx`
- **Госпитализация** — запись и просмотр по коду (диагноз, цель, отделение)
- **Направления на процедуры** — интерфейс врача с авторизацией, просмотр данных пациента и медкарты
- **Веб-интерфейс** на Jinja2 и REST API со Swagger UI

## 🧱 Стек

| Технология | Роль |
|---|---|
| Python 3.12, FastAPI, Uvicorn | API и веб-сервер |
| SQLAlchemy 2 (async) | ORM; по умолчанию SQLite через `aiosqlite` |
| Alembic | миграции БД (`alembic.ini` указывает на `app/migration`) |
| Jinja2 + HTML/CSS/JS | интерфейс |
| qrcode, OpenCV, docxtpl | QR-коды и `.docx`-документы |
| pydantic-settings | конфигурация из `.env` |
| Docker | контейнеризация (`Dockerfile`) |

## 🗂 Структура проекта

```
app/
├── main.py              # FastAPI-приложение
├── config.py, database.py, logger.py, exception.py
├── dao/                 # базовый DAO-слой
├── patients/            # пациенты: модели, схемы, роутер, авторизация
├── doctors/             # врачи
├── hospitalization/     # госпитализации
├── med_procedure/       # лечебно-диагностические мероприятия
├── pages/               # HTML-страницы
└── templates/, static/  # шаблоны и JS
openapi.yml              # спецификация API
```

## 🚀 Быстрый старт

Создайте `.env` в корне проекта (переменные — ниже), затем:

```bash
git clone https://github.com/Edvvard0/med_services.git
cd med_services
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Docker:

```bash
docker build -t med_services .
docker run -p 8000:8000 med_services
```

Swagger UI: http://127.0.0.1:8000/docs

> В репозитории нет каталога `app/migration`, на который ссылается `alembic.ini`, поэтому миграции может потребоваться сгенерировать самостоятельно: `alembic revision --autogenerate -m "Initial migration"`. Для запуска в Docker `.env` нужно передать в контейнер (например, `--env-file .env`) или положить в образ.

## ⚙️ Конфигурация

| Переменная | Назначение |
|---|---|
| `DB_URL` | строка подключения (по умолчанию SQLite `data/db.sqlite3` в корне проекта) |
| `API_HOST`, `API_PORT` | хост и порт API (обязательны) |
| `LOG_LEVEL` | уровень логирования (обязательна) |
| `SECRET_KEY` | секрет для подписи JWT (обязательна) |
| `ALGORITHM` | алгоритм подписи JWT (обязательна) |

## 🔌 API

Спецификация — [`openapi.yml`](openapi.yml). Основные группы: `/patients`, `/doctors`, `/hospitalizations`, `/med_procedure`, `/pages` (HTML-интерфейс).

## 🗺 Планы

- Рефакторинг: убрать дублирование кода, вынести общую логику в базовые классы
- Хранение фото и документов в S3 вместо локальных файлов
- Переход с SQLite на PostgreSQL
- Веб-часть для скачивания договоров и согласий
- Строгая валидация данных на уровне Pydantic и API
- Собственные классы исключений
- Скрипт автозаполнения тестовыми данными
- Проверка занятости кабинетов при записи на процедуры

<!-- TODO: скриншот интерфейса -->

## 👤 Автор

**Эдвард Осипчук** — [GitHub @Edvvard0](https://github.com/Edvvard0) · [Telegram @Edward0076](https://t.me/Edward0076)
