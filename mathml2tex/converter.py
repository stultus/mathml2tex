import os
import re

import nh3
from bs4 import BeautifulSoup, NavigableString
from lxml import etree

_ALLOWED_TAGS = {
    "a", "b", "br", "code", "em", "i", "img", "li", "ol", "p", "pre", "span",
    "strong", "sub", "sup", "table", "tbody", "td", "th", "thead", "tr", "u", "ul",
}
_ALLOWED_ATTRS = {
    "a": {"href", "title"},
    "img": {"src", "alt", "class", "style", "title", "width", "height"},
    "*": {"class"},
}


def _sanitize_html(html):
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


def convert_mathml2tex(equation):
    '''Convert MathML to LaTeX.

    ref: https://github.com/oerpub/mathconverter
    '''
    dom = etree.fromstring(equation, parser=_PARSER)
    newdom = _TRANSFORM(dom)
    latex = re.sub(r'^\$+|\$+$', '', str(newdom).strip()).strip()
    return latex


def sanitize_statement(statement):
    '''Sanitize statement with MathML into TeX and minimal HTML.

    Each <math> block in the input is replaced inline with its LaTeX
    equivalent, wrapped in \\( ... \\) delimiters. The rest of the HTML
    is run through nh3 with a safe allowlist.
    '''
    soup = BeautifulSoup(statement, features="html.parser")
    for item in soup.find_all('math'):
        latex = convert_mathml2tex(str(item))
        item.replace_with(NavigableString(rf"\( {latex} \)"))
    return _sanitize_html(str(soup)).strip()
