# Проект AGROтур
### Описание
Благодаря этому проекту можно создать аккаунт и делиться постами агротуров с другими пользователями, выкладывать их в тематические группы, оставлять комментарии под постами, а также подписываться на других пользователей.

### Инструкция по развёртыванию/использованию
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AndrejKazakov/git@github.com:AndrejKazakov/project_yatube.git
```

```
cd project_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
Выполнить миграции:
```
python yatube/manage.py migrate
```

Запустить проект:
```
python yatube/manage.py runserver
```


### Системные требования
Это приложение написано на языке Python версии 3.8. Для запуска приложения необходимо установить следующие зависимости:

Django версии 2.2
