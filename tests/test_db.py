from pathlib import Path
import pickle
from jane_watson import db, util
import pandas as pd
from jane_watson.db import kbai


def test_extract_text_from_subtitle():
    path = "/Volumes/Mac/OMSCS/09___Case_Based_Reasoning_subtitles/" \
           "231 - Exercise_ Retrieval by Discrimin. Tree Solution.srt"
    text = db.extract_text_from_subtitle(path)
    util.print_limit(text)


def test_summarize_in_bullets():
    path = "/Volumes/Mac/OMSCS/15___Commonsense_Reasoning_subtitles/" \
           "400 - Example_ Ashok Ate a Frog.srt"
    text = db.extract_text_from_subtitle(path)
    summary = db.summarize_in_bullets(text)
    util.print_limit(summary)


def test_summarize_in_bullets_2():
    path1 = "/Volumes/Mac/OMSCS/13___Planning_subtitles/" \
            "347 - Exercise_ Goals Question.srt"
    text1 = db.extract_text_from_subtitle(path1)
    path2 = "/Volumes/Mac/OMSCS/13___Planning_subtitles/" \
            "348 - Exercise_ Goals Solution.srt"
    text2 = db.extract_text_from_subtitle(path2)
    text = text1 + '\n' + text2
    summary = db.summarize_in_bullets(text)
    util.print_limit(summary)


def test_get_embeddings():
    path = "/Volumes/Mac/OMSCS/15___Commonsense_Reasoning_subtitles/" \
           "400 - Example_ Ashok Ate a Frog.srt"
    text = db.extract_text_from_subtitle(path)
    embeddings = db.get_embeddings(text)
    print(embeddings)


def test_extract_module():
    path = '/Volumes/Mac/OMSCS/01___Intro_to_Knowledge_Based_AI_subtitles'
    data = db.extract_module(path, 348259, 62750)
    with Path('/tmp/planning.pkl').open('wb') as f:
        pickle.dump(data, f)


def test_extract_course():
    path = '/Volumes/Mac/OMSCS'
    data = db.extract_course(path)
    with Path('/tmp/kbai.pkl').open('wb') as f:
        pickle.dump(data, f)


def test_load():
    with Path('/tmp/kbai.pkl').open('rb') as f:
        data = pickle.load(f)
    db.load(data)


def test_answer():
    query = "What is Means Ends analysis?"
    a = db.answer(query)
    print(a)


def test_module():
    results = pd.DataFrame(kbai.find({}))
    print(len(results))
