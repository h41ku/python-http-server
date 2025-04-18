# Что это?

Этот проект создан в целях изучения Python и его возможностей для организации веб-серверов на микроконтроллерах.

Это не какой-то готовый продукт, инструмент, библиотека или фреймворк.
Разработка и исследование все еще продолжается. Не используйте его в промышленных разработках.

## Требования

Для запуска требуется наличие Python версии 3 и выше или MicronPython.
Установка зависит от операционной системы.

## Запуск

Запуск в окружении системы:

```sh
python3 ./index.py
```

Запуск в виртуальном окружении:

```sh
# при необходимости можете создать виртуально окружение
# python -m venv $PATH_TO_VENV

# активация виртуального окружение
source $PATH_TO_VENV/bin/activate

# запуск сервера
python3 ./index.py
```

## Нагрузочный тест

Для тестирования этого сервера рекомендуется использовать утилиту Apache Bench.
Установите ее, если ее еще нет в системе.

```sh
# для систем на базе Debian
apt install -y apache2-utils

# для Alpine
apk add apache2-utils

# для систем на базе RedHat
yum install -y httpd-tools
```

Запустите сервер. Затем запустите тест:

```sh
ab -n 50000 -c 10 -s 120 http://127.0.0.1:3080/
```

Прочитайте больше по аргументу командной строки, чтобы настроить тест под ваше окружение.

## Лицензия

MIT

## Планы

* Читать параметры запуска сервера из конфигурационного файла
* Внедрить концепцию промежуточного ПО
* Промежуточное ПО для передачи статики
* Виртуальная маршрутизация
* Автозагрузка контроллеров из отдельных модулей
