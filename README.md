# up_trader
Тестовое задание для UpTrader

## Задача:
Нужно сделать django app, который будет реализовывать древовидное меню, соблюдая следующие условия:

1. Меню реализовано через template tag
2. Все, что над выделенным пунктом - развернуто. Первый уровень вложенности под выделенным пунктом тоже развернут.
3. Хранится в БД.
4. Редактируется в стандартной админке Django
5. Активный пункт меню определяется исходя из URL текущей страницы
6. Меню на одной странице может быть несколько. Они определяются по названию.
7. При клике на меню происходит переход по заданному в нем URL. URL может быть задан как явным образом, так и через named url.
8. На отрисовку каждого меню требуется ровно 1 запрос к БД.

Нужен django-app, который позволяет вносить в БД меню (одно или несколько) через админку, и нарисовать на любой нужной странице меню по названию.
```{% draw_menu 'main_menu' %}```

При выполнении задания из библиотек следует использовать только Django и стандартную библиотеку Python.

## Установка
Требуется установить и запустить виртуальное окружение, и установить фрейморк Django
```
python -m venv venv
. venv/bin/activate
pip install django
```
В репозитории имеется БД на SQLite, в которой находятся тестовые данные. Данные суперпользователя: логин - admin, email - admin@admin.ru, пароль - admin

## Использование древовидного меню
Для того, чтобы отрисовать меню в шаблоне необходимо:

1. Создать меню и элементы меню в БД админки Django (настроена и создан суперпользователь)
2. В шаблоне Django загрузить приложение и вызвать TAG `draw_menu :menu_name:` -> `menu_name` - наименование меню, по которому оно вызывается

```
{# ЗАГРУЖАЕМ ПРИЛОЖЕНИЕ #}
{% load treeview %}

<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title></title>
</head>
<body>

{# ОТРОСОВЫВАЕМ ШАБЛОН, ИСПОЛЬЗУЯ ТЭГ draw_menu #}
{% draw_menu 'main' as main_menu %}
{{ main_menu|safe }}

{% draw_menu 'not_main' as not_main_menu %}
{{ not_main_menu|safe }}

</body>
</html>
```

## Скриншот
![SCREEN](https://github.com/shakertov/up_trader/blob/main/images/1.png)
