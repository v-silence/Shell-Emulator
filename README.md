# Эмулятор UNIX-подобной оболочки
Данный проект представляет собой эмулятор UNIX-подобной оболочки, который позволяет воссоздать сеанс работы в командной строке UNIX-подобной операционной системы. Эмулятор запускается из реальной командной строки и работает с виртуальной файловой системой, упакованной в архив формата tar.

## Описание
Эмулятор принимает конфигурационный файл в формате YAML, который содержит следующие параметры:

hostname - имя компьютера, которое будет отображаться в приглашении к вводу.
fs_path - путь к архиву с виртуальной файловой системой в формате tar.
log_path - путь к файлу лога в формате XML.
startup_script_path - путь к стартовому скрипту, который будет выполнен при запуске эмулятора.
Лог-файл в формате XML содержит все действия, выполненные во время последнего сеанса работы с эмулятором.

Стартовый скрипт служит для начального выполнения заданного списка команд из файла.

## Эмулятор поддерживает следующие команды:

- ls - вывод списка файлов и каталогов в текущем каталоге.
- cd - смена текущего каталога.
- exit - выход из эмулятора.
- pwd - вывод абсолютного пути к текущему каталогу.
- tail - вывод последних строк из файла.
- du - отображение размера файлов и каталогов.
## Требования
Для работы эмулятора необходимо наличие следующих компонентов:

- Python 3.6 или новее
- PyYAML
- pytest (для запуска тестов)

## Установка
- ### Клонируйте репозиторий с проектом:
https://github.com/v-silence/Shell-Emulator.git
- ### Перейдите в директорию проекта:
cd Shell-Emulator
- ### Установите необходимые зависимости
