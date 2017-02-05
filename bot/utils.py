code_mapping = (
    ("'", '&#39;'),
    ('"', '&quot;'),
    ('>', '&gt;'),
    ('<', '&lt;'),
    ('«', '&laquo;'),
    ('»', '&raquo;'),
    (' ', '&nbsp;'),
    ('—', '&#151;'),
    ('&', '&amp;'),
)


def html_decode(s):
    for code, escaped in code_mapping:
        s = s.replace(escaped, code)

    return s
