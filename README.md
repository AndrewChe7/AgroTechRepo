# Маркетплейс

Данное приложение реализует базовый функционал маркетплейса. Возможна регистрация следующих пользователей:
* Поставщики
* Закупщики оптовые
* Закупщики розничные
* Перевозчики

### Поставщики
Могут выкладывать товары с ценами для разных размеров опта, просматривать существующие заказы закупщиков и делиться информацией в своем блоге

### Закупщики
Могут просматривать товары поставщиков, покупать их и выкладывать заказы на товары, а также подписываться на блоги поставщиков. Розничные покупатели тоже могут покупать товары и следить за интересующими фермерскими хозяйствами.

### Перевозчики
Могут отслеживать договоры между поставщиками и закупщиками, выполнять заказы на перевозку.

## Установка
``` bash
pip install -r requirements.txt
export DJANGO_SECRET=ключ
export DJANGO_DB=ИМЯ БАЗЫ ДАННЫХ
export DJANGO_DB_USER=ИМЯ ПОЛЬЗОВАТЕЛЯ БД
export DJANGO_DB_PASSWORD=ПАРОЛЬ БД
export STATIC_ROOT=/путь/к/статичным/файлам
gunicorn AgroHackMarketplace.wsgi
```

## Демо
Для работы приложение использует heroku.
