# shell python
## описание
Простая файловая оболочка (shell), реализованная на Python. 
Она имитирует базовые команды работы с файлами и каталогами. 
Также реализована корзина для удаленных файлов и логи для просмотра истории действий.

## алгоритм работы программы

программа инициализирует ядро, которое выполняет все программы, подающиеся на вход. 
далее программа вызывает функцию которая сканирует и добавляет команды в ядро.
затем бесконечный ввод команд из терминала которые подаются в логи и в ядро, там парсятся, выполняются, а в случае ошибки обрабатываются и заносятся в логи.

## команды

### 1. cat
вывод содержимого файла
```
cat <path> 
```

### 2. cd 
изменение рабочей директории 
```
cd <path='~'>
```

### 3. cp
копирование файла или директории в указанное место
```
cp <source_path> <destination_path> [-r]
```

### 4. exit
завершение программы
```
exit
```
### 5. ls
вывод содержимого директории
```
ls <path='.'> [-l]
```
### 6. mv
перемещение файла или директории в указанное место
```
mv <source_path> <destination_path>
```
### 7. pwd
вывод пути до рабочей директории
```
pwd
```
### 8. rm
удаление файла или директории
```
rm <source_path> [-r]
```
## Установка и запуск
1. Убедитесь, что у вас установлен Python 3.13 или выше
2. Скачайте репозиторий:
```bash
git clone https://github.com/Kopylovvv/shell_python.git
cd shell_python
```
3. Создайте и активируйте виртуальное окружение:
```bash
uv venv
source .venv/bin/activate
```
4. Установите зависимости:
```bash
uv sync
```
5. Запустите программу:
```bash
python -m src.main
```

## структура
```
├── .trash/
├── pyproject.toml
├── README.md
├── shell.log
├── src
│   ├── __init__.py
│   ├── commands
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── cat.py
│   │   ├── cd.py
│   │   ├── cp.py
│   │   ├── exit.py
│   │   ├── ls.py
│   │   ├── mv.py
│   │   ├── pwd.py
│   │   └── rm.py
│   ├── core.py
│   ├── main.py
│   └── utils
│       ├── __init__.py
│       ├── console_info.py
│       ├── error_decorator.py
│       ├── format_output.py
│       ├── logger.py
│       └── parser.py
├── tests
│   ├── __init__.py
│   ├── test_cat_command.py
│   ├── test_cd_command.py
│   ├── test_core.py
│   ├── test_cp_command.py
│   ├── test_ls_command.py
│   ├── test_mv_command.py
│   └── test_rm_command.py
└── uv.lock
```
