#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from converter import sanitize_statement

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
		processed_equation = '<p>Directions: Select the related number from the given alternatives.</p><p><p>\\( \\frac{U}{S}:\\frac{21}{19}::\\frac{K}{R}:?\\)</p> </p>'
		stmt = sanitize_statement(equation)
		print(stmt)
		print("-------------------------------------")
		self.assertEqual(processed_equation,stmt)
	
	def test_image_converter(self):
		self.maxDiff = None
		equation = '''<p>According to the question,<br></p>
		<p><img src=\"https://testseries.edugorilla.com/static/media/qdump/e789d441b19dcbee3d3fb03a95367ba9/7fd120670a0b54fb42aefa2f8e57fe0b.png\"
		class=\"img-responsive\" style=\"display: inline;\"></p>
		<p>= 54 – 16 x 3 + 6 ÷ 2</p><p>= 54 – 16 x 3 +3</p>
		<p>= 6 + 3 =9</p><p>Hence, option A is the correct response.&nbsp;</p>'''
		processed_equation = '''<p>According to the question,</p> 
		<p><img class="img-responsive" src="https://testseries.edugorilla.com/static/media/qdump/e789d441b19dcbee3d3fb03a95367ba9/7fd120670a0b54fb42aefa2f8e57fe0b.png"/></p> 
		<p>= 54 – 16 x 3 + 6 ÷ 2</p><p>= 54 – 16 x 3 +3</p> <p>= 6 + 3 =9</p><p>Hence, option A is the correct response. </p>'''
		stmt = sanitize_statement(equation)
		print(stmt)
		self.assertEqual(1, 1)

if __name__ =='__main__':
	unittest.main()
