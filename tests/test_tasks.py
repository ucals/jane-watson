from pathlib import Path
import pickle
from jane_watson import tasks, util


def test_extract_text_from_subtitle():
    path = "/Volumes/Mac/OMSCS/15___Commonsense_Reasoning_subtitles/" \
           "400 - Example_ Ashok Ate a Frog.srt"
    text = tasks.extract_text_from_subtitle(path)
    util.print_limit(text)


def test_summarize_in_bullets():
    path = "/Volumes/Mac/OMSCS/15___Commonsense_Reasoning_subtitles/" \
           "400 - Example_ Ashok Ate a Frog.srt"
    text = tasks.extract_text_from_subtitle(path)
    summary = tasks.summarize_in_bullets(text)
    util.print_limit(summary)


def test_summarize_in_bullets_2():
    path1 = "/Volumes/Mac/OMSCS/13___Planning_subtitles/" \
            "347 - Exercise_ Goals Question.srt"
    text1 = tasks.extract_text_from_subtitle(path1)
    path2 = "/Volumes/Mac/OMSCS/13___Planning_subtitles/" \
            "348 - Exercise_ Goals Solution.srt"
    text2 = tasks.extract_text_from_subtitle(path2)
    text = text1 + '\n' + text2
    summary = tasks.summarize_in_bullets(text)
    util.print_limit(summary)


def test_get_embeddings():
    path = "/Volumes/Mac/OMSCS/15___Commonsense_Reasoning_subtitles/" \
           "400 - Example_ Ashok Ate a Frog.srt"
    text = tasks.extract_text_from_subtitle(path)
    embeddings = tasks.get_embeddings(text)
    print(embeddings)


def test_ingest_module():
    path = '/Volumes/Mac/OMSCS/13___Planning_subtitles'
    data = tasks.ingest_module(path, 348715, 62762)
    with Path('/tmp/planning.pkl').open('wb') as f:
        pickle.dump(data, f)

