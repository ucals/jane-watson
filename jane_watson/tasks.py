from pathlib import Path
from time import sleep

import openai
from tqdm import tqdm

from jane_watson.db import kbai


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


def summarize_in_bullets(text, retries=5, sleep_between_retries=1):
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Class transcript:\n{text}\n\n\n"
                               f"Summarize this class in bullet points."
                }],
                temperature=0,
                max_tokens=256,
            )
            return response.choices[0].message.content
        except openai.error.ServiceUnavailableError as e:
            sleep(sleep_between_retries)
            print(f'Retrying {i + 1} of {retries}, {str(e)}')
    raise Exception(f'Failed to summarize {text}')


def get_embeddings(text, retries=5, sleep_between_retries=1):
    for i in range(retries):
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except openai.error.ServiceUnavailableError as e:
            sleep(sleep_between_retries)
            print(f'Retrying {i + 1} of {retries}, {str(e)}')
    raise Exception(f'Failed to summarize {text}')


def extract_module(
        module_path,
        first_class_id,
        module_id,
        course_id=39458,
        show_progress=False
):
    module_path = Path(module_path)
    module_name = module_path.stem.split('___')[1]\
        .replace('_', ' ').replace(' subtitles', '')

    files = sorted(list(module_path.glob('*.srt')))
    pbar = tqdm(files) if show_progress else files
    data = []
    for i, str_file in enumerate(pbar):
        class_name = str_file.stem.split(' - ')[1]
        if show_progress:
            pbar.set_postfix(class_name=class_name, module_name=module_name)
        if class_name.endswith('Question'):
            continue
        if class_name.endswith('Solution'):
            solution = extract_text_from_subtitle(str_file)
            question = extract_text_from_subtitle(str(files[i - 1]))
            text = f'{question}\n{solution}'
        else:
            text = extract_text_from_subtitle(str_file)

        summary = summarize_in_bullets(text)
        text_for_embeddings = f'Class title: {class_name}\n\n' \
                              f'Module: {module_name}\n\n' \
                              f'Class summary:\n{summary}\n\n' \
                              f'Class transcript:\n{text}'
        embeddings = get_embeddings(text_for_embeddings)
        url = f'https://edstem.org/us/courses/{course_id}/lessons' \
              f'/{module_id}/slides/{first_class_id + i}'
        data.append({
            'module': module_name,
            'class': class_name,
            'summary': summary,
            'transcript': text,
            'embeddings': embeddings,
            'url': url
        })
    return data


def extract_course(
        course_path,
        first_class_id=348259,
        first_module_id=62750,
        course_id=39458
):
    course_path = Path(course_path)
    modules_paths = sorted(list(course_path.glob('*___*_subtitles')))
    data = []
    fcid = first_class_id
    for i, module_path in enumerate(modules_paths):
        module_name = module_path.stem.split('___')[1]\
            .replace('_', ' ').replace(' subtitles', '')
        print(f'Extracting module {i + 1}: {module_name}...')
        module_id = first_module_id + i
        module_data = extract_module(
            module_path,
            first_class_id=fcid,
            module_id=module_id,
            course_id=course_id
        )
        data += module_data
        fcid += len(module_data) + 1
    return data


def load(data):
    kbai.insert_many(data)
