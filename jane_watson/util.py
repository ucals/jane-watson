from pathlib import Path


def extract_text_from_subtitle(subtitle_path):
    with Path(subtitle_path).open('r') as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            with Path(subtitle_path).open('r', encoding='latin-1') as g:
                lines = g.readlines()

        text = ""
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.isnumeric():
                i += 2
                continue
            if line == "":
                i += 1
                continue
            text += line + " "
            i += 1

    return text


def print_limit(text, line_limit=80):
    text = text.replace('\n', ' <br/> ')
    words = text.split(' ')
    line = words.pop(0)
    while len(words) > 0:
        word = words.pop(0)
        if len(word) == 0:
            continue
        if word == '<br/>':
            print(line)
            line = words.pop(0)
            continue

        if len(line) + len(word) > line_limit:
            print(line)
            line = word
        else:
            line = f'{line} {word}'
    if len(line) > 0:
        print(line)
