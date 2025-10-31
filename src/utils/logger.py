import logging
import pathlib


def get_logger(file: pathlib.Path) -> logging.Logger:
    """
    создает и настраивает логгер с записью в указанный файл
    если логгер уже был создан, то возвращаяется имеющийся

    Args:
        file (pathlib.Path): путь к файлу с логами

    Returns:
        logging.Logger: настроенный логгер
    """

    logger = logging.getLogger() # корневой логгер

    if not logger.handlers: # проверка на наличие обработчиков
        # создание форматтера для определения структуры сообщений логгера
        # %(asctime)s - время события
        # %(levelname)s - уровень логирования
        # %(message)s - текст сообщения
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler = logging.FileHandler(file) # создание обработчика для записи логов
        handler.setFormatter(formatter) # установка форматтера

        logger.addHandler(handler) # добавление обработчика к логгеру
        logger.setLevel(logging.INFO) # установка уровеня логирования - обработка сообщений уровня INFO и выше

    return logger