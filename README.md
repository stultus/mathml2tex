# mathml2tex

Convert MathML to LaTeX. A thin Python wrapper around Vasil Yaroshevich's
XSLT 1.0 stylesheet (`xsltml`, now bundled under `mathml2tex/xsl_yarosh/`),
with inline-HTML sanitization on top for mixed content such as quiz
statements or textbook passages.

See [`HISTORY.md`](HISTORY.md) for the provenance of the bundled stylesheets.

## Install

```sh
pip install mathml2tex
```

## Usage

### As a library

```python
from mathml2tex import convert_mathml2tex, sanitize_statement

mathml = (
    '<math xmlns="http://www.w3.org/1998/Math/MathML">'
    '<mfrac><mi>a</mi><mi>b</mi></mfrac>'
    '</math>'
)
convert_mathml2tex(mathml)
# -> '\\frac{a}{b}'

html = f'<p>The ratio is {mathml}.</p>'
sanitize_statement(html)
# -> '<p>The ratio is \\( \\frac{a}{b} \\).</p>'
```

`convert_mathml2tex` accepts either `str` or `bytes`. On invalid input it
raises `mathml2tex.converter.Mathml2TexError`.

`sanitize_statement` takes HTML containing zero or more `<math>` blocks,
replaces each block with its LaTeX equivalent wrapped in `\( ... \)`
delimiters, and runs the result through [nh3](https://pypi.org/project/nh3/)
with an allowlist suited to educational content. Pass `strict=False` to
log-and-skip unconvertible blocks instead of raising.

### As a CLI

```sh
mathml2tex equation.xml                 # standalone MathML → LaTeX
cat page.html | mathml2tex --html       # HTML with inline <math> → sanitized HTML
echo "$MATHML" | mathml2tex             # from stdin
```

## Security

The XML parser is configured to reject external entities and network
fetches; the XSLT transform denies all I/O access. MathML from untrusted
sources is safe to hand directly to `convert_mathml2tex`.

## Compatibility

- Python 3.8+
- lxml 4.9+ (4.x or 5.x or 6.x)

## License

MIT. See `LICENSE`. The bundled `xsl_yarosh/` stylesheets carry their own
permissive license from Vasil Yaroshevich, preserved in each file header.
