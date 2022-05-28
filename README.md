# Parliamone!

This repository contains the content and source code for the website [Parliamone!][].

Most of the code comes from [Schedario Napoletano][sn] (same author).

[Parliamone!]: https://www.parliamone-conversazione.it

[sn]: https://github.com/schedario-napoletano/website

## Setup

    poetry install

## Tests

    poetry run pytest

## Config

* `QUESTIONS_URL`: if defined, questions are loaded from this URL
* `CANONICAL_DOMAIN`
* `HTTPS`: set it to use HTTPS
* `TOKEN`: token for the admin route to reload the questions
