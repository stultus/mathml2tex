from __future__ import annotations

import logging
import os
import re
from typing import Union

import nh3
from bs4 import BeautifulSoup, NavigableString
from lxml import etree

logger = logging.getLogger(__name__)

_MATHML_NS = "http://www.w3.org/1998/Math/MathML"

_ALLOWED_TAGS = {
    "a", "b", "br", "code", "em", "i", "img", "li", "ol", "p", "pre", "span",
    "strong", "sub", "sup", "table", "tbody", "td", "th", "thead", "tr", "u", "ul",
}
_ALLOWED_ATTRS = {
    "a": {"href", "title"},
    "img": {"src", "alt", "class", "style", "title", "width", "height"},
    "*": {"class"},
}


class Mathml2TexError(Exception):
    """Raised when MathML input cannot be converted to LaTeX."""


def _sanitize_html(html: str) -> str:
    return nh3.clean(html, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRS)


_HERE = os.path.dirname(os.path.realpath(__file__))
_XSLT_PATH = os.path.join(_HERE, 'xsl_yarosh', 'mmltex.xsl')

_PARSER = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    huge_tree=False,
    load_dtd=False,
)
_TRANSFORM = etree.XSLT(
    etree.parse(_XSLT_PATH),
    access_control=etree.XSLTAccessControl.DENY_ALL,
)


def _coerce_mathml_bytes(equation: Union[str, bytes]) -> bytes:
    if isinstance(equation, bytes):
        return equation
    if isinstance(equation, str):
        return equation.encode("utf-8")
    raise Mathml2TexError(
        f"MathML input must be str or bytes, got {type(equation).__name__}"
    )


def convert_mathml2tex(equation: Union[str, bytes]) -> str:
    """Convert a MathML string or bytes payload to a LaTeX string.

    ref: https://github.com/oerpub/mathconverter
    """
    payload = _coerce_mathml_bytes(equation)
    try:
        dom = etree.fromstring(payload, parser=_PARSER)
    except etree.XMLSyntaxError as exc:
        raise Mathml2TexError(f"invalid MathML: {exc}") from exc
    root_tag = etree.QName(dom.tag)
    if root_tag.namespace != _MATHML_NS:
        raise Mathml2TexError(
            "root element is not in the MathML namespace "
            f"({_MATHML_NS!r}); add xmlns=\"{_MATHML_NS}\" on <math>"
        )
    try:
        newdom = _TRANSFORM(dom)
    except etree.XSLTApplyError as exc:
        raise Mathml2TexError(f"XSLT transform failed: {exc}") from exc
    return re.sub(r'^\$+|\$+$', '', str(newdom).strip()).strip()


def sanitize_statement(statement: str, *, strict: bool = True) -> str:
    """Sanitize a statement with inline MathML into TeX + minimal HTML.

    Each ``<math>`` block is replaced inline with its LaTeX equivalent
    wrapped in ``\\( ... \\)`` delimiters. The rest of the HTML is
    allowlist-sanitized with nh3.

    When ``strict`` is True (the default) a failed MathML conversion
    propagates as ``Mathml2TexError``. When False, the offending
    ``<math>`` block is logged and left in the output untouched.
    """
    soup = BeautifulSoup(statement, features="html.parser")
    for item in soup.find_all('math'):
        try:
            latex = convert_mathml2tex(str(item))
        except Mathml2TexError:
            if strict:
                raise
            logger.warning("skipping unconvertible <math> block", exc_info=True)
            continue
        item.replace_with(NavigableString(rf"\( {latex} \)"))
    return _sanitize_html(str(soup)).strip()
