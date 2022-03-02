

def is_camel(name: str) -> bool:
    for char in name:
        if char.isupper():
            return True
    return False


def is_snake(name: str) -> bool:
    for char in name:
        if char.isupper():
            return False
    return True


def camel_to_snake(name: str) -> str:
    word = ''
    words = []
    upper = False
    for char in name:
        if char.isupper():
            if upper:
                word += char
            else:
                words.append(word)
                word = char
            upper = True
        else:
            if word.isupper() and len(word) > 1:
                words.append(word[:-1])
                word = word[-1].lower()
            word += char
            upper = False
    words.append(word)

    # remove ''
    words = [word if word.isupper() else word.lower() for word in words if word]

    return '_'.join(words)


def snake_to_camel(name: str) -> str:
    result = ''
    upper = False
    for char in name:
        if char == '_':
            upper = True
            continue
        else:
            if upper:
                char_upper = char.upper()
                result += char_upper
                upper = False
            else:
                result += char
    return result


def class_name(name: str) -> str:
    if is_camel(name):
        return name[:1].upper() + name[1:]

    if is_snake(name):
        return class_name(snake_to_camel(name))

    raise Exception('Unknown Name Format!')
