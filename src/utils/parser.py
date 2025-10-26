def parse_object(string: str) -> dict:

    tokens = string.split()
    if tokens:
        options = []
        args = ''
        for token in tokens[1:]:
            if token[0] == '-':
                for option in token[1:]:
                    options.append(option)
            else:
                args = token
        command_params = {"command_name": tokens[0], "arguments": args, "options": options}
        return command_params
    return {"command_name": '', "arguments": '', "options": []}