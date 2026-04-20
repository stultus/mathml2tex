import os

from setuptools import setup

_here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(_here, "README.md"), encoding="utf-8") as _readme:
    long_description = _readme.read()

setup(
    name="mathml2tex",
    version="0.3",
    packages=["mathml2tex"],
    license="MIT",
    author="Hrishikesh Bhaskaran",
    author_email="hrishi.kb@gmail.com",
    url="https://github.com/stultus/mathml2tex",
    description="Convert MathML (inline or standalone) to LaTeX via XSLT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mathml latex mathml2latex xslt",
    python_requires=">=3.8",
    install_requires=["lxml>=4.9,<7", "beautifulsoup4>=4.9", "nh3>=0.2"],
    package_data={"mathml2tex": ["xsl_yarosh/*.xsl", "xsl_yarosh/README*"]},
    include_package_data=True,
    entry_points={
        "console_scripts": ["mathml2tex=mathml2tex.__main__:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Text Processing :: Markup :: XML",
    ],
)
