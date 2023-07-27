from pathlib import Path
import openai
import os
from tqdm import tqdm


def extract_text_from_subtitle(subtitle_path):
    with Path(subtitle_path).open('r') as f:
        lines = f.readlines()
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


def summarize_in_bullets(text):
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


def get_embeddings(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']


def ingest_module(module_path, first_class_id, module_id, course_id=39458):
    module_path = Path(module_path)
    module_name = module_path.stem.split('___')[1].replace('_', ' ')

    files = sorted(list(module_path.glob('*.srt')))
    pbar = tqdm(files)
    data = []
    for i, str_file in enumerate(pbar):
        class_name = str_file.stem.split(' - ')[1]
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
