# Банковское API
Это API для банковского приложения, разработанное с использованием Django Rest Framework (DRF). В нем реализованы функции управления счетами, 
проведения транзакций между счетами пользователя в долларах и рублях и множество других функций для удобного и безопасного взаимодействия с банковскими операциями.  

## Технологии
Проект использует следующие технологии и инструменты:

- Django — основной веб-фреймворк для разработки.
- Django Rest Framework (DRF) — для создания RESTful API.
- Djoser — для авторизации и регистрации пользователей с использованием email.
- Celery — для асинхронной обработки задач.
- Flower — для мониторинга задач Celery в реальном времени.
- RabbitMQ — брокер сообщений для Celery.
- Redis — кэширование данных для улучшения производительности.
- PostgreSQL — база данных для хранения данных приложения.
- Docker — для контейнеризации и управления зависимостями (Redis, RabbitMQ, и других сервисов).

## Функции

### Авторизация с использованием Djoser:
Для регистрации и аутентификации пользователей используется библиотека Djoser.  
Авторизация через email вместо username, где при регистрации указываются следующие поля:  
- email
- username
- first_name
- last_name
- password

### Управление счетами:

Создание счета: Каждый пользователь может создать несколько типов счетов с выбором из двух валют (Доллар, Рубль):  
- Текущий
- Сберегательный
- Кредитный

Редактирование счета: Возможность обновить информацию о счете.  
Удаление счета: Пользователь может удалить счет, если он больше не нужен.   

### Транзакции:

Депозит: Пополнение счета.  
Снятие средств: Перевод средств с одного счета на другой.  
Перевод между счетами: Осуществление перевода между счетами одного пользователя.  
Тип транзакции указывается в теле запроса через поле type. Поддерживаемые типы:  
- deposit — депозит на счет.
- withdraw — снятие средств с счета.
- transfer — перевод между счетами. 

### Асинхронная обработка транзакций:
- Подключен Celery для асинхронной обработки транзакций, таких как переводы и другие ресурсоемкие операции.  
Используется RabbitMQ в качестве брокера сообщений для управления задачами Celery.  

### Кэширование:  
- Подключен Redis для кэширования информации о счетах и транзакциях, что улучшает производительность API.  

### Мониторинг задач Celery с помощью Flower:
- Для мониторинга задач Celery используется Flower — инструмент, который позволяет отслеживать состояние задач и рабочих процессов Celery в реальном времени.

## Установка

1. Клонирование репозитория
```bash
git clone git@github.com:ShantiBB/bank_app.git
cd bank_app
```

2. Установка зависимостей
Для управления зависимости испльзуется poetry
```bash
pip install poetry
poetry install
```

3. Настройка базы данных
   
  Примените миграции для создания необходимых таблиц в базе данных:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Настройка RabbitMQ, Redis, Celery и Flower
   
Запуск Redis и RabbitMQ через Docker
```bash
docker run -d -p 6379:6379 redis
docker run -d -p 5672:5672 rabbitmq
```

  Для запуска Celery и Flower:  

Запустите рабочий процесс Celery:
```bash
celery -A core.celery_app worker -l info
```

Запустите Flower для мониторинга задач Celery:
```bash
celery -A core.celery_app flower
```

Теперь Flower доступен по адресу: http://localhost:5555.  

5. Запуск сервера
   
  Запустите сервер разработки:
```bash
python manage.py runserver
```  
Теперь приложение доступно по адресу: http://127.0.0.1:8000.

## API Endpoints  
API доступно по пути api/v1/.

### Авторизация и регистрация
- POST /api/v1/users/ - Регистрация нового пользователя (через email)
- POST /api/v1/auth/login/ - Логин пользователя (возвращает токен)
- POST /api/v1/auth/logout/ - Логин пользователя
  
### Управление счетами
- POST /api/v1/accounts/ - Создать новый счет
- GET /api/v1/accounts/ - Получить список счетов
- GET /api/v1/accounts/{id}/ - Получить информацию о счете
- PUT /api/v1/accounts/{id}/ - Обновить счет
- DELETE /api/v1/accounts/{id}/ - Удалить счет

### Транзакции
- POST /api/v1/transactions/ - Осуществить транзакцию (депозит, снятие или перевод)
- POST /api/v1/transactions/ - Получить историю транзакций
- POST /api/v1/transactions/{id}/ - Удалить транзакцию из истории

## Дополнительные улучшения и будущие разработки:
- Поддержка конвертации валют по текущему курсу.  
- Переводы на счета других пользователей.
- Отправка истории транзакций на email.
- Уведомление об успешной транзакции на email.
