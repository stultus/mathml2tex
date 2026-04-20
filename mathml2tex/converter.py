#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import nh3
from bs4 import BeautifulSoup
from lxml import etree

_ALLOWED_TAGS = {
    "a", "b", "br", "code", "em", "i", "img", "li", "ol", "p", "pre", "span",
    "strong", "sub", "sup", "table", "tbody", "td", "th", "thead", "tr", "u", "ul",
}
_ALLOWED_ATTRS = {
    "a": {"href", "title", "rel"},
    "img": {"src", "alt", "class", "style", "title", "width", "height"},
    "*": {"class"},
}


def _sanitize_html(html):
    return nh3.clean(html, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRS)

def convert_mathml2tex(equation):
    '''Convert MathML to Latex
    ref: https://github.com/oerpub/mathconverter
    '''
    script_base_path = os.path.dirname(os.path.realpath(__file__))
    xslt_file = os.path.join(script_base_path, 'xsl_yarosh', 'mmltex.xsl')
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    equation = str(newdom)
    equation = equation.replace('$', '').strip()
    return equation


def sanitize_statement(statement):
    ''' Sanitize statement with MathML 
    into Tex & minimul html'''
    soup = BeautifulSoup(statement, features="lxml")
    for item in soup.find_all('math'):
        new_tag = soup.new_tag('p')
        latex_string = convert_mathml2tex(str(item))
        new_tag.string = f"\( {latex_string}\)"
        item.replace_with(new_tag)
    #for x in soup.find_all():
    #    if len(x.get_text(strip=True)) == 0:
    #        x.extract()
    converted_equation = " ".join(str(soup).split())
    return _sanitize_html(converted_equation).strip()
    
	
