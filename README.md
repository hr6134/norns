```
npm i  # ставим пакеты
npm run build # собираем фронт и кладёт его в папку статики django
pipenv shell
pipenv install
./manage.py runserver # запускает django
```

креды меняем в функции `_get_auth` в файле `/norns/urd/views.py`