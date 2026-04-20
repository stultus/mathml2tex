# mathml2tex

A thin Python wrapper around Vasil Yaroshevich's XSLT 1.0 stylesheet
(`xsltml`, bundled under `mathml2tex/xsl_yarosh/`) that converts
**MathML 2.0** to **LaTeX**, with optional inline-HTML sanitization for
mixed content such as quiz statements or textbook passages.

See [`HISTORY.md`](HISTORY.md) for the provenance of the bundled stylesheets.

## Status: maintenance mode

The underlying XSLT stylesheet (`xsltml`) was last released in **2007** and
only targets **MathML 2.0**. It does not support MathML 3.0 elements
(`mlongdiv`, `mstack`, `maction`, `mlabeledtr`, `mscarries`) and has no
real Content MathML coverage for modern inputs.

This package still works well for its original use case — converting
Presentation MathML 2.0 fragments, with HTML sanitization on top — and
has been hardened for security (XXE/SSRF-safe parsing, nh3 allowlist,
100% test coverage). **If that's your use case, use it.**

If you need any of the following, pick an actively-maintained alternative
from the list below:
- MathML 3 / MathML 4 elements
- Robust Content MathML support
- A larger community / more momentum behind the tool

## Alternatives

| Tool | Language | MathML version | Notes |
| --- | --- | --- | --- |
| [`mathml-to-latex`](https://pypi.org/project/mathml-to-latex/) | Python (pure) | 2 + partial 3 | Drop-in PyPI alternative, actively maintained. **Recommended for most new projects.** |
| [Pandoc](https://pandoc.org/) (`texmath`) | Haskell | 2 + 3 | General-purpose document converter; MathML→LaTeX is one of many paths. |
| [`transpect/mml2tex`](https://github.com/transpect/mml2tex) | XSLT 2.0 | 2 + 3 | Actively-maintained descendant of `xsltml`; requires a Saxon (Java) runtime. Includes a Content→Presentation normalizer. |

## Install

```sh
pip install mathml2tex
```

## Usage

### Library

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

`convert_mathml2tex` accepts `str` or `bytes`. Invalid MathML, missing
namespace, or transform failures raise `mathml2tex.converter.Mathml2TexError`.

`sanitize_statement` replaces each inline `<math>` block with its LaTeX
equivalent wrapped in `\( ... \)`, then allowlist-sanitizes the result
with [nh3](https://pypi.org/project/nh3/). Pass `strict=False` to skip
and log unconvertible blocks instead of raising.

### CLI

```sh
mathml2tex equation.xml                 # standalone MathML → LaTeX
cat page.html | mathml2tex --html       # HTML with inline <math>
echo "$MATHML" | mathml2tex             # from stdin
```

## Security

The XML parser rejects external entities and network fetches; the XSLT
transform denies all I/O (`XSLTAccessControl.DENY_ALL`). MathML from
untrusted sources is safe to hand directly to `convert_mathml2tex`.

## Compatibility

- Python 3.8+
- lxml 4.9+ (supports lxml 4.x, 5.x, 6.x)

## License

MIT. See `LICENSE`. The bundled `xsl_yarosh/` stylesheets carry their
own permissive license from Vasil Yaroshevich, preserved in each file
header.
