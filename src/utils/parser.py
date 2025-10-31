import shlex


def parse_object(string: str) -> dict:
    """
    парсер для команд
    выделяет имя команды, аргументы (поддержка ввода через пробел в кавычках) и флаги
    Args:
        string (str): строка, содержащая команду
    Returns:
        dict: словарь из трех элементов: имя команды (str), аргументы (list[str]), флаги (list[str])
    """
    tokens = shlex.split(string) # разделение по пробелам вне кавычек
    if tokens:
        args = [] # список для аргументов
        options = [] # список для флагов
        for token in tokens[1:]:
            if token[0] == '-': # проверка на флаг
                for option in token[1:]:
                    options.append(option)
            else:
                args.append(token)
        command_params = {"command_name": tokens[0], "arguments": args, "options": options}
        return command_params
    return {"command_name": '', "arguments": [], "options": []}
