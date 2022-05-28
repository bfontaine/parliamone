from typing import List, Dict
from urllib.parse import urlparse

import htmlmin
from flask import Flask, render_template, abort, redirect, request
from flask_assets import Environment
from webassets import Bundle

from parliamone import config, utils
from parliamone.utils import count_questions

app = Flask(__name__)
app.jinja_options["autoescape"] = lambda _: True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

QUESTIONS: Dict[str, List[str]] = {}


def load_questions():
    global QUESTIONS
    QUESTIONS = utils.load_questions()


if config.HTTPS or config.CANONICAL_DOMAIN:
    @app.before_request
    def redirect_to_canonical_domain():
        url_parts = urlparse(request.url)
        if url_parts.netloc != config.CANONICAL_DOMAIN:
            url_parts = url_parts._replace(netloc=config.CANONICAL_DOMAIN)
        if config.HTTPS and url_parts.scheme != "https":
            url_parts = url_parts._replace(scheme="https")

        new_url = url_parts.geturl()
        if new_url != request.url:
            return redirect(new_url, code=301)


@app.after_request
def minify_html(response):
    if not app.debug and response.content_type.startswith("text/html"):
        response.set_data(
            htmlmin.minify(response.get_data(as_text=True),
                           remove_comments=True,
                           remove_empty_space=True)
        )

    return response


assets = Environment(app)
# js = Bundle(...,
#             filters='jsmin', output='static/js/main.min.js')
# assets.register('js_all', js)

sass = Bundle('sass/main.scss', filters='libsass', output='css/sass.css')
all_css = Bundle(sass, filters='rcssmin', output="css/main.min.css")
assets.register('css_all', all_css)


@app.route("/")
def home():
    count = count_questions(QUESTIONS)
    questions_count_more_than = (count // 50) * 50

    return render_template("home.html.j2",
                           categories=[
                               {"slug": utils.get_category_slug(category),
                                "title": utils.get_category_title(category)}
                               for category in sorted(QUESTIONS)
                           ],
                           categories_count=len(QUESTIONS),
                           questions_count_more_than=questions_count_more_than)


@app.route("/domande/<slug>")
def category_page(slug):
    category = slug.replace("_", " ")

    if category not in QUESTIONS:
        abort(404)

    title = utils.get_category_title(category)
    questions = QUESTIONS[category]

    questions_a = questions[::2]
    questions_b = questions[1::2]

    return render_template("category.html.j2",
                           category_title=title,
                           sub_title=title,
                           category_lower_title=category,
                           questions_a=questions_a,
                           questions_b=questions_b)


@app.route("/a-proposito")
def about():
    return render_template("about.html.j2")


# Admin
@app.route("/reload", methods=["POST"])
def reload():
    token = request.args.get('token')
    if token != config.TOKEN:
        abort(403)

    load_questions()
    return f"loaded {count_questions(QUESTIONS)} questions in {len(QUESTIONS)} categories."


#
load_questions()
