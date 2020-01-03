#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from lxml import etree
from bs4 import BeautifulSoup
from htmllaundry import sanitize

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
    return sanitize(converted_equation).strip()
    
	
