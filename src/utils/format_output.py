def format_table(data: list[list[str]]) -> str:
    """
    Форматирует данные в виде таблицы без разделителей.
    Ширина каждого столбца определяется по самому длинному элементу в нем.

    Args:
        data: список списков, где каждый вложенный список - строка таблицы

    Returns:
        str: отформатированная таблица в виде строки
    """
    if not data:
        return ""

    # Определяем максимальную длину для каждого столбца
    num_columns = len(data[0])
    column_widths = [0] * num_columns

    for row in data:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))

    # Форматируем таблицу
    formatted_lines = []
    for row in data:
        formatted_cells = []
        for i, cell in enumerate(row):
            # Выравниваем каждую ячейку по левому краю с учетом максимальной ширины столбца
            formatted_cell = str(cell).ljust(column_widths[i])
            formatted_cells.append(formatted_cell)
        formatted_lines.append(" ".join(formatted_cells))

    return "\n".join(formatted_lines)