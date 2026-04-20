import logging

import pytest
from lxml import etree

from mathml2tex import convert_mathml2tex, sanitize_statement
from mathml2tex.converter import (
    Mathml2TexError,
    _coerce_mathml_bytes,
    _sanitize_html,
)

NS = 'xmlns="http://www.w3.org/1998/Math/MathML"'
FRAC = f'<math {NS}><mfrac><mi>a</mi><mi>b</mi></mfrac></math>'


class TestCoerceMathmlBytes:
    def test_passes_bytes_through(self):
        assert _coerce_mathml_bytes(b"<math/>") == b"<math/>"

    def test_encodes_str_as_utf8(self):
        assert _coerce_mathml_bytes("<math/>") == b"<math/>"

    def test_encodes_non_ascii_str(self):
        assert _coerce_mathml_bytes("αβ") == "αβ".encode("utf-8")

    def test_rejects_other_types(self):
        with pytest.raises(Mathml2TexError, match="must be str or bytes"):
            _coerce_mathml_bytes(42)


class TestConvertMathml2Tex:
    def test_bytes_input(self):
        assert convert_mathml2tex(FRAC.encode()) == r"\frac{a}{b}"

    def test_str_input(self):
        assert convert_mathml2tex(FRAC) == r"\frac{a}{b}"

    def test_strips_wrapping_dollars_and_whitespace(self):
        out = convert_mathml2tex(FRAC)
        assert not out.startswith("$")
        assert not out.endswith("$")
        assert out == out.strip()

    def test_preserves_interior_dollars(self, monkeypatch):
        class _FakeResult:
            def __str__(self):
                return "$\\text{price: \\$5}$"

        monkeypatch.setattr(
            "mathml2tex.converter._TRANSFORM",
            lambda dom: _FakeResult(),
        )
        assert convert_mathml2tex(FRAC) == "\\text{price: \\$5}"

    def test_raises_on_malformed_xml(self):
        with pytest.raises(Mathml2TexError, match="invalid MathML"):
            convert_mathml2tex(b"<math><not closed")

    def test_raises_on_missing_namespace(self):
        bare = b"<math><mfrac><mi>a</mi><mi>b</mi></mfrac></math>"
        with pytest.raises(Mathml2TexError, match="namespace"):
            convert_mathml2tex(bare)

    def test_raises_on_wrong_type(self):
        with pytest.raises(Mathml2TexError, match="must be str or bytes"):
            convert_mathml2tex(3.14)

    def test_raises_on_xslt_failure(self, monkeypatch):
        def _boom(dom):
            raise etree.XSLTApplyError("forced")

        monkeypatch.setattr("mathml2tex.converter._TRANSFORM", _boom)
        with pytest.raises(Mathml2TexError, match="XSLT transform failed"):
            convert_mathml2tex(FRAC.encode())

    def test_xxe_entity_not_resolved(self):
        payload = (
            b'<?xml version="1.0"?>'
            b'<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>'
            b'<math xmlns="http://www.w3.org/1998/Math/MathML">'
            b'<mi>&xxe;</mi></math>'
        )
        out = convert_mathml2tex(payload)
        assert "/etc/passwd" not in out
        assert "root:" not in out


class TestSanitizeStatement:
    def test_plain_html_passes_through(self):
        assert sanitize_statement("<p>hello</p>") == "<p>hello</p>"

    def test_converts_inline_math(self):
        html = f"<p>x = {FRAC}</p>"
        out = sanitize_statement(html)
        assert r"\( \frac{a}{b} \)" in out
        assert "<math" not in out

    def test_does_not_nest_paragraphs(self):
        html = f"<p>x = {FRAC}</p>"
        out = sanitize_statement(html)
        assert "<p><p>" not in out
        assert out.count("<p>") == 1

    def test_converts_multiple_math_blocks(self):
        html = f"<p>{FRAC} and {FRAC}</p>"
        out = sanitize_statement(html)
        assert out.count(r"\frac{a}{b}") == 2

    def test_preserves_pre_whitespace(self):
        html = "<pre>line1\n  line2</pre>"
        out = sanitize_statement(html)
        assert "line1\n  line2" in out

    def test_strips_scripts(self):
        out = sanitize_statement("<p>hi<script>alert(1)</script></p>")
        assert "<script" not in out
        assert "alert(1)" not in out

    def test_strict_mode_propagates_errors(self):
        bad = "<p><math><mi>x</mi></math></p>"
        with pytest.raises(Mathml2TexError):
            sanitize_statement(bad, strict=True)

    def test_non_strict_mode_skips_and_logs(self, caplog):
        bad = "<p>before <math><mi>x</mi></math> after</p>"
        with caplog.at_level(logging.WARNING, logger="mathml2tex.converter"):
            out = sanitize_statement(bad, strict=False)
        assert any(
            "skipping unconvertible" in r.message for r in caplog.records
        )
        # nh3 strips the unknown <math> tag but keeps its text.
        assert "before" in out and "after" in out

    def test_empty_input_returns_empty(self):
        assert sanitize_statement("") == ""


class TestSanitizeHtmlHelper:
    def test_allows_p(self):
        assert _sanitize_html("<p>x</p>") == "<p>x</p>"

    def test_strips_div(self):
        assert "<div" not in _sanitize_html("<div>x</div>")
