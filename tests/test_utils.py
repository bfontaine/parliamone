from parliamone import utils


def test_parse_question_line():
    assert utils.parse_question_line("[foo] What?") == (("foo",), "What?")
    assert utils.parse_question_line("[foo,bar] What?") == (("foo", "bar"), "What?")
    assert utils.parse_question_line("[ foo, bar ] What?") == (("foo", "bar"), "What?")
    assert utils.parse_question_line("[ ping-pong, varietà, il più e il meno] What?") == \
           (("ping-pong", "varietà", "il più e il meno"), "What?")
