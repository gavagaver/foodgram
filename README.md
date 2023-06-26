# Foodgram - кулинарная соцсеть

Foodgram - веб-приложение, которое поможет приготовить вкусную еду, предоставляя доступ к рецептам сообщества увлеченных кулинаров. Каждый пользователь может создавать рецепты, указывая необходимые ингредиенты. Есть возможность сохранять понравившиеся рецепты, а также создавать списки покупок на основе выбранных рецептов и подписываться на любимых авторов.

## Установка и запуск
1. [ ] Клонируем репозиторий 
```bash
 git clone git@github.com:gavagaver/foodgram-project-react.git 
```
1. [ ] Выполняем вход на удаленный сервер
2. [ ] Устанавливаем на сервере docker
```bash
apt install docker.io 
```
1. [ ] Устанавливаем на сервере docker-compose
```bash
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
1. [ ] Создаем и запускаем docker-контейнеры
``` 
docker-compose up -d --build 
```
1. [ ] Создаем миграции
``` 
docker-compose exec web python manage.py makemigrations 
```
1. [ ] Применяем миграции
``` 
docker-compose exec web python manage.py migrate 
``` 
1. [ ] Создаем суперпользователя
``` 
docker-compose exec web python manage.py createsuperuser 
``` 
1. [ ] Собираем статику
``` 
docker-compose exec web python manage.py collectstatic --no-input 
``` 

## Стек
- Python 3.7
- Django 3.2
- PostgreSQL
- gunicorn
- nginx
- Яндекс.Облако (Ubuntu 20.04)

## Об авторе
Голишевский Андрей Вячеславович  
Python-разработчик (Backend)  
E-mail: gav@gaver.ru  
Telegram: @gavagaver  
Россия, г. Москва  
