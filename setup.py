from setuptools import setup

setup(
    name='mathml2tex',
    version='0.3',
    packages=['mathml2tex'],
    license='The MIT License (MIT)',
    author='Hrishikesh Bhaskaran',
    author_email='hrishi.kb@gmail.com',
    url='http://stultus.in',
    description='Convert semi html statements with MathML to semi html statements with Latex',
    long_description=open('README.md').read(),
    keywords='mathml latex mathml2latex ',
    install_requires=['lxml>=4.9,<7', 'beautifulsoup4>=4.9', 'nh3>=0.2'],
    package_data={'mathml2tex': ['xsl_yarosh/*.xsl', 'xsl_yarosh/README*']},
    include_package_data=True,
)

