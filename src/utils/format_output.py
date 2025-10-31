def format_table(data: list[list[str]]) -> str:
    """
    форматирует данные в виде таблицы без разделителей
    чтобы ширина каждого столбца была равна наибольшей длине в этом столбце

    Args:
        data (list[list[str]]): список списков, где каждый вложенный список - строка таблицы

    Returns:
        str: отформатированная таблица в виде строки
    """
    if not data:
        return ""

    # максимальная длина для каждого столбца
    num_columns = len(data[0])
    column_widths = [0] * num_columns
    for row in data:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))

    # форматирование таблицы
    formatted_lines = []
    for row in data:
        formatted_cells = []
        for i, cell in enumerate(row):
            # выравнивание каждой ячейки по левому краю с учетом ширины через ljust
            formatted_cell = str(cell).ljust(column_widths[i])
            formatted_cells.append(formatted_cell)
        formatted_lines.append(" ".join(formatted_cells))

    return "\n".join(formatted_lines)
