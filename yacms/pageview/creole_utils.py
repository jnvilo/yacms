# coding: utf-8


"""
    python creole utilities
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyleft: 2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals

import shlex

from creole.py3compat import TEXT_TYPE, PY3

try:
    from pygments import lexers
    from pygments.formatters import HtmlFormatter
    PYGMENTS = True
except ImportError:
    PYGMENTS = False


# For string2dict()
KEYWORD_MAP = {
    "True": True,
    "False": False,
    "None": None,
}


def get_pygments_formatter():
    if PYGMENTS:
        return HtmlFormatter(lineos = True, encoding='utf-8',
                             style='colorful', outencoding='utf-8',
                             cssclass='pygments')


def get_pygments_lexer(source_type, code):
    if PYGMENTS:
        try:
            return lexers.get_lexer_by_name(source_type)
        except:
            return lexers.guess_lexer(code)
    else:
        return None


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
