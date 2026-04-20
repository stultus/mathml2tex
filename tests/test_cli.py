import os

import pytest

from mathml2tex.__main__ import main

NS = 'xmlns="http://www.w3.org/1998/Math/MathML"'
FRAC = f'<math {NS}><mfrac><mi>a</mi><mi>b</mi></mfrac></math>'


class TestCli:
    def test_stdin_standalone_math(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", _StringIO(FRAC))
        assert main([]) == 0
        out = capsys.readouterr().out
        assert r"\frac{a}{b}" in out

    def test_stdin_html_with_math_auto_detect(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", _StringIO(f"<p>x = {FRAC}</p>"))
        assert main([]) == 0
        out = capsys.readouterr().out
        assert r"\( \frac{a}{b} \)" in out
        assert "<p>" in out

    def test_html_flag_forces_sanitize_path(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", _StringIO(FRAC))
        assert main(["--html"]) == 0
        out = capsys.readouterr().out
        assert r"\( \frac{a}{b} \)" in out

    def test_file_input(self, tmp_path, capsys):
        p = tmp_path / "eq.xml"
        p.write_text(FRAC, encoding="utf-8")
        assert main([str(p)]) == 0
        assert r"\frac{a}{b}" in capsys.readouterr().out

    def test_invalid_input_returns_nonzero(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", _StringIO("<math><not closed"))
        rc = main([])
        assert rc == 1
        err = capsys.readouterr().err
        assert "mathml2tex:" in err


class _StringIO:
    def __init__(self, text):
        self._text = text

    def read(self):
        return self._text
