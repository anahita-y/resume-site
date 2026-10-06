import re
from django import template

register = template.Library()

_SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

_LATIN_RUN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9@._/:+#%&=?~\- ]*[A-Za-z0-9/.])?")


def _escape(text):
    return "".join(_SPECIAL.get(ch, ch) for ch in text)


@register.filter
def tex(value):
    text = re.sub(r"\s*[\r\n]+\s*", " ", str(value or "")).strip()
    out = []
    pos = 0
    for m in _LATIN_RUN.finditer(text):
        out.append(_escape(text[pos:m.start()]))
        out.append(r"\lr{" + _escape(m.group()) + "}")
        pos = m.end()
    out.append(_escape(text[pos:]))
    return "".join(out)