#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from converter import convert_mathml2tex

class ConverterTestClass(unittest.TestCase):
	'''Test mathml2tex'''

	def test_converter(self):
		equation = '''<div class=\"dquizquestion\"><p>Directions: Select the related number
		from the given alternatives.</p><p><span class=\"mathMlContainer\" 
		contenteditable=\"false\"><math xmlns=\"http://www.w3.org/1998/Math/MathML\">
		<mfrac><mi>U</mi><mi>S</mi></mfrac><mo>:</mo><mfrac><mn>21</mn><mn>19</mn></mfrac>
		<mo>:</mo><mo>:</mo><mfrac><mi>K</mi><mi>R</mi></mfrac><mo>:</mo><mo>?</mo></math>
		</span><br></p></div><div class=\"dsubquesquestion\" data-subquesno=\"0\">
		<div class=\"dsubquesquestion\" data-subquesno=\"0\">
		<div class=\"dsubquesquestion\" data-subquesno=\"0\">
		<div class=\"dsubquesquestion\" data-subquesno=\"0\" <=\"\" div=\"\"><label class=\"quizlabel no_hover\">
		<div class=\"labelDiv container\"></div></label></div></div></div></div>'''
		processed_equation = '''<p>Directions: Select the related number
                from the given alternatives. </p>
                <p>\frac{U}{S}:\frac{21}{19}::\frac{K}{R}:?</p> '''
		self.assertEqual(convert_mathml2tex(equation), processed_equation)

if __name__ =='__main__':
	unittest.main()
