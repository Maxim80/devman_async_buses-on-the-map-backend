# Автобусы на карте Москвы
Веб-приложение показывает передвижение автобусов по карте Москвы.
![](.buses.gif)

## Как установить
Сначала необходимо установить [фронтенд](https://github.com/devmanorg/buses-on-the-map.git):
```
git clone git@github.com:devmanorg/buses-on-the-map.git
```
Затем установить сам проект:
```
git clone git@github.com:Maxim80/devman_async_buses-on-the-map-backend.git
```
## Как запустить
Для запуска фронтенда нужно открыть в браузере файл `index.html`, который находится в корневой папке.

Для запуска проекта  необходимо запустить скрипт `server.py`:
```
python server.py
```
Дополнительные аргументы:
`--bus_port` - порт на который сервер будет принимать данные о автобусах, по умолчанию 8080.
`--browser_port` - порт на который должны подключаться клиенты(фронтенд), по умолчанию 8000.
`--debug` - включить debug, по умолчанию отключен.

 Для имитации автобусов нужно запустить скрипт `fake_bus.py`, который имитирует передвижение автобусов генерируя их координаты:
 ```
 python fake_bus.py
 ```
 Дополнительные аргументы:
 `--server` - IP :порт сервера на который отправлять координаты автобусов, по умолчанию `127.0.0.1:8080`.
 `--routes_number` - количество маршрутов, по умолчанию 100.
 `--buses_per_route` - количество автобусов на маршруте, по умолчанию 5.
 `--websockets_number` - количество открытых веб-сокетов, по умолчанию 10.
 `--emulator_id` - префикс автобусов в случае запуска нескольких экземпляров симулятора.
 `--refresh_timeout` - таймаут между обновлением координат автобуса, по умолчанию 0,3 секунды.
 `--debug` - включить debug, по умолчанию отключен.

 ## Цели проекта
 Проект написан в учебных целях в рамках курса по python-программированию на сайте [Devman](https://dvmn.org/).
