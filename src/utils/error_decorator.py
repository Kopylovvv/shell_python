from functools import wraps


def error_handler(logger):
    """
    декоратор для обработки ошибок в функциях с логированием
    перехватывает исключения в декорируемой функции, выводит их в консольи записывает в логгер

    Args:
        logger: объект логгера для записи ошибок

    Returns:
        function: декоратор для обертывания функций
    """

    def decorator(func):
        """
        внутренний декоратор, принимающий целевую функцию

        Args:
            func: функция, которую нужно обернуть
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            обертка функции

            Returns:
                результат выполнения оригинальной функции
            """

            # попытка выполнить функцию
            try:
                return func(*args, **kwargs)

            # обработка ошибок
            except (FileNotFoundError, NotADirectoryError, PermissionError, SyntaxError) as e:
                print(e) # вывод ошибки в консоль
                logger.error(e)  # запись в лог

        return wrapper
    return decorator