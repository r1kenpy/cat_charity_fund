## Описание проекта
Сервис позволяет собирать пожертвования для помощи котикам.
Пользователь может зарегистрироваться и совершить пожертвовать любую сумму. 
Сделать пожертвование можно даже если сейчас нет активного проекта. Сумма будет зачислена в след открытый проект.
Создать проект может только супер пользователь.
Суперпользователь будет создан автоматически, если данные будут указаны в env файле.

### Стек:
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### Эндпоинты проекта

В проеке есть 3 эсновные категории эндпоинтов.

### Projects:

- Просмотр существующих проектов. GET запрос на `/charity_project/` - может любой пользователь
- Создание проекта. POST запрос на `/charity_project/` - достпен только суперпользователю.
- Удаление или редактирование проекта. PATCH или DELETE запрос на  `/charity_project/{project_id}` - достпен только суперпользователю.

### Donations:
- Полная информация о пожертвовании. GET запрос на `/donation/` - достпен только суперпользователю.
- Совершить пожертвование. POST запрос на `/donation/` - доступен любому авторизованному пользователю.
- Просмотр собственных пожертвований. GET запрос на `/donation/my` - доступен любому авторизованному пользователю.

Подробную информацию об эндпоинтах можно посмотреть локально после запуска проекта в [документации](http://127.0.0.1:8000/docs#/)


### Как развернуть проект

- Клонируем проект командой `git clone git@github.com:r1kenpy/cat_charity_fund.git`;
- Переходим в папку проекта `cd cat_charity_fund`;
- Создаем виртуальное окружение командой `python3 -m venv venv` если у вас Linux/macOS или `python -m venv venv` если у вас windows;
- Активируем виртуальное окружение:
  - Если у вас Linux/macOS `source venv/bin/activate`;
  - Если у вас windows `source venv/scripts/activate`.
- Устанавливаем зависимости командой `pip install -r requirements.txt`
- Создаем файл `.env`:
- В env файл нужно добавить: 
  - APP_TITLE - Заголовок проекта для документации;
  - DATABASE_URL - Ссылка для связи с базой данных;
  - SECRET - Переменная для хеширования паролей;
  - FIRST_SUPERUSER_EMAIL - Эмейл суперпользователя;
  - FIRST_SUPERUSER_PASSWORD - Пароль суперпользователя.
- Применяем миграции `alembic upgrade head`;
- Запускаем проект `uvicorn app.main:app --reload`;
- Переходим на странице документации [Swagger](http://127.0.0.1:8000/docs#/) или [ReDoc](http://127.0.0.1:8000/redoc).

#### Автор [Молчанов Владимир](https://t.me/r1ken0)