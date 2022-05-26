import re
from collections import defaultdict
from typing import List, Dict, Tuple

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


def load_questions(min_by_category=4):
    questions: Dict[str, List[str]] = defaultdict(list)

    with open("questions.txt") as f:
        for line in f:
            categories, question = parse_question_line(line)
            for category in categories:
                questions[category].append(question)

    total = 0

    for category in list(questions):
        category_questions = questions[category]
        category_count = len(category_questions)
        if category_count < min_by_category:
            print(f"Removing {category_count} questions from category '{category}';"
                  f" they are fewer than {min_by_category}.")
            del questions[category]
            continue
        total += category_count

    print(f"Loaded {total} questions in {len(questions)} categories.")
    return dict(questions)
