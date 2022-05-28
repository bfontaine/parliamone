import os.path

ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
QUESTIONS_FILE = os.path.join(ROOT_PATH, "questions.txt")
QUESTIONS_URL = os.environ.get("QUESTIONS_URL")
CANONICAL_DOMAIN = os.environ.get("CANONICAL_DOMAIN")
HTTPS = os.environ.get('HTTPS')
TOKEN = os.environ.get('TOKEN', 'secret')
