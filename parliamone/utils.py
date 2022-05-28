import re
from collections import defaultdict
from typing import List, Dict, Tuple, TextIO
from urllib.error import HTTPError
from urllib.request import urlopen

from parliamone.config import QUESTIONS_FILE, QUESTIONS_URL

question_line_re = re.compile(r"^\[([^]]*)]\s*(.+)$")


def parse_question_line(line: str) -> Tuple[Tuple[str, ...], str]:
    match = question_line_re.match(line)
    assert match
    tags_str = match.group(1)
    question = match.group(2).strip()

    tags = [tag.strip() for tag in tags_str.split(",")]
    return tuple(tags), question


def get_category_title(category: str):
    return category.capitalize()


def get_category_slug(category: str):
    return category.replace(" ", "_")


def _load_questions_from_reader(f: TextIO):
    questions: Dict[str, List[str]] = defaultdict(list)

    with open(QUESTIONS_FILE) as f:
        for line in f:
            categories, question = parse_question_line(line)
            for category in categories:
                questions[category].append(question)

    return dict(questions)


def _trim_questions(questions: Dict[str, List[str]], min_by_category=4):
    for category in list(questions):
        category_questions = questions[category]
        category_count = len(category_questions)
        if category_count < min_by_category:
            print(f"Removing {category_count} questions from category '{category}';"
                  f" they are fewer than {min_by_category}.")
            del questions[category]
            continue


def count_questions(questions):
    return sum(len(qs) for qs in questions.values())


def load_raw_questions():
    if QUESTIONS_URL:
        print(f"loading from {QUESTIONS_URL}")
        try:
            with urlopen(QUESTIONS_URL) as response:
                return _load_questions_from_reader(response)
        except HTTPError as e:
            print(e)

    with open(QUESTIONS_FILE) as f:
        print("loading from file")
        return _load_questions_from_reader(f)


def load_questions(min_by_category=4):
    questions = load_raw_questions()
    _trim_questions(questions, min_by_category=min_by_category)

    print(f"Loaded {count_questions(questions)} questions in {len(questions)} categories.")
    return dict(questions)
