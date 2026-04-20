# History and Provenance of `xsl_yarosh`

This document records the historical origins of the XSLT stylesheets contained in this repository. The upstream URL referenced inside every stylesheet header and in the `README` file, <http://www.raleigh.ru/MathML/mmltex>, is no longer resolvable. Because this URL predates most modern archives of MathML tooling and appears verbatim in dozens of downstream projects, it is worth preserving an account of what it was, who maintained it, and why the code under `mathml2tex/xsl_yarosh/` exists in the form it does.

## The author: Vasil I. Yaroshevich

The stylesheets were written by **Vasil I. Yaroshevich**, a Russian software developer active in the early 2000s MathML community. He maintained the project under the short name **`xsltml`** ("XSLT MathML Library"). The name Yaroshevich uses for the work in publications and on mailing lists is rendered both as "Vasil Yaroshevich" and "Vasil I. Yaroshevich"; the copyright notice in the source files uses the shorter form.

Yaroshevich was not affiliated with the W3C Math Working Group, but his library was one of the earliest pure-XSLT solutions to a problem the Working Group had explicitly flagged as open: how to convert MathML back into LaTeX without requiring a compiled program or a platform-specific extension. His decision to implement the conversion entirely in XSLT 1.0, using only standard features and no processor extensions, is the reason the library continues to run unmodified in 2025 on Xalan, Saxon, libxslt, and every other conformant XSLT 1.0 engine.

In a 2011 message to the W3C `www-math` mailing list, Yaroshevich confirmed the project was no longer maintained:

> I've written stylesheets for converting mathml formulas into latex notation: xsltml.sourceforge.net — but now I don't support it.

No successor release has appeared since. Version **2.1.2**, dated around 2007, remains the final release.

## The original distribution site: `www.raleigh.ru/MathML/mmltex`

Prior to moving to SourceForge, Yaroshevich hosted the project on a personal or organisational site under the `raleigh.ru` domain. The canonical entry points were:

- `http://www.raleigh.ru/MathML/mmltex/` — project landing page (English and Russian versions at `index.php?lang=en` and `index.php?lang=ru`).
- `http://www.raleigh.ru/MathML/mmltex/online.php` — an interactive online converter where a user could paste a MathML expression and receive LaTeX output in the same page. This converter is referenced in Pavi Sandhu's *The MathML Handbook* (Charles River Media, 2003) as the recommended way to experiment with the stylesheets without installing an XSLT processor locally.
- `http://www.raleigh.ru/MathML/mmltex/mmltex.zip` and later `http://www.raleigh.ru/MathML/mmltex/xsltml_2.1.2.zip` — the downloadable stylesheet bundle.

The `raleigh.ru` host is unrelated to the city of Raleigh, North Carolina. It was a generic Russian domain under which the MathML project was one of several subsites. The domain is no longer under the original registrant and the MathML content is not preserved on it today. The only remaining trace of the URL is the comment block at the top of every `xsl_yarosh` stylesheet in this repository:

```xml
<!-- $Id: mmltex.xsl 441 2007-09-16 23:21:16Z fletcher $
     This file is part of the XSLT MathML Library distribution.
     See ./README or http://www.raleigh.ru/MathML/mmltex for
     copyright and other information                       -->
```

Subsequent to the `raleigh.ru` site going offline, the project was relocated to SourceForge at <https://sourceforge.net/projects/xsltml/> and <https://xsltml.sourceforge.net/>. The SourceForge release `xsltml_2.1.2.zip` is byte-compatible with the final `raleigh.ru` zip and is the source from which this repository's `xsl_yarosh` directory was taken.

## What the library does

`xsltml` is a set of six XSLT 1.0 stylesheets that together translate any valid **Presentation MathML 2.0** document into equivalent **LaTeX** source. The six files are:

- `mmltex.xsl` — top-level entry point. It `xsl:include`s the other five files and is the only stylesheet that needs to be referenced by a calling pipeline.
- `tokens.xsl` — transforms MathML token elements (`<mi>`, `<mn>`, `<mo>`, `<mtext>`, `<ms>`) into their LaTeX equivalents, including operator spacing and font selection.
- `glayout.xsl` — general layout schemata (`<mrow>`, `<mfrac>`, `<msqrt>`, `<mroot>`, `<mstyle>`, `<merror>`, `<mpadded>`, `<mphantom>`, `<mfenced>`, `<menclose>`).
- `scripts.xsl` — sub- and super-scripts and under-/over-scripts (`<msub>`, `<msup>`, `<msubsup>`, `<munder>`, `<mover>`, `<munderover>`, `<mmultiscripts>`).
- `tables.xsl` — matrix and table constructs (`<mtable>`, `<mtr>`, `<mtd>`, `<mlabeledtr>`, alignment scopes).
- `entities.xsl` — maps MathML named character entities and many Unicode mathematical code points to LaTeX macros, including the symbol sets that require `amssymb`, `amsmath`, `amsfonts`, or `stmaryrd`.

The library was designed to produce LaTeX that compiles under a standard `article` class with `amsmath`, `amssymb`, and `amsfonts` loaded. It handles Presentation MathML only; Content MathML is not supported and was never implemented, despite occasional announcements at the time suggesting it might be.

## Why the library mattered historically

When `xsltml` was first released in 2001–2002, MathML 2.0 had just reached W3C Recommendation status (21 February 2001), and the set of tools capable of round-tripping between MathML and LaTeX was very small. The three serious options were:

1. **David Carlisle's `xmltex` / `pmml2tex`** — required TeX itself as the processing engine, which made it unusable in XML-only pipelines.
2. **The ORCCA group's Java converter** (University of Western Ontario, Stephen Watt's group) — a compiled Java program, not embeddable in XSLT-based publishing chains.
3. **Yaroshevich's `xsltml`** — pure XSLT 1.0, no extensions, no runtime dependency other than an XSLT processor.

The third option was the only one that fit cleanly into the XML-first publishing pipelines that scientific publishers, textbook platforms, and early ebook systems were building at the time. This is the reason `xsltml` shows up embedded, forked, or adapted inside a disproportionate number of downstream projects:

- **Fletcher Penney's MultiMarkdown** (MMD 2.0) vendored `mmltex.xsl` to give Markdown authors LaTeX output from their equations.
- **`mml2tex`** by transpect.io is a modernised XSLT 2.0 descendant that still credits Yaroshevich's library as its starting point.
- **OERPUB's `mathconverter`** includes `xsl_yarosh` as one of its pluggable conversion back-ends.
- **ActiveMath** (Paul Libbrecht et al.) used a heavily adjusted fork of these stylesheets as the rendering core of its notation system.
- **Connexions / OpenStax / Rhaptos** used Yaroshevich-derived XSLT in their EPUB MathML-to-text and MathML-to-LaTeX fallbacks.
- The W3C Math Working Group's own `implementations.html` page listed `xsltml` as a reference implementation for MathML-to-LaTeX conversion.

The `raleigh.ru` URL therefore functions as a kind of fossil marker: any stylesheet in the wild that still carries that comment in its header can be traced back, directly or through one or more forks, to Yaroshevich's original 2001–2003 release.

## License

The work is distributed under what is effectively an MIT-style permissive licence. The original `README` states:

> Copyright (C) 2001–2003 Vasil Yaroshevich
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> Except as contained in this notice, the names of individuals credited with contribution to this software shall not be used in advertising or publicity relating to the Software without specific prior written permission.

This licence is compatible with the MIT licence under which this repository is published.

## Version history (upstream)

The upstream project published a small number of releases. Dates below are reconstructed from the `$Id:` keyword expansions embedded in the source files and from the SourceForge release timestamps.

| Version | Approximate date | Notes |
|---|---|---|
| 1.0   | 2001 | Initial release on `raleigh.ru`. Presentation MathML subset. |
| 2.0   | 2002 | Copyright notice updated; listed by W3C as a reference implementation. |
| 2.1   | 2003 | `entities.xsl` expanded; matches the release referenced in Sandhu, *The MathML Handbook*. |
| 2.1.2 | 2007 | Final release. Minor fixes to `scripts.xsl` and `tables.xsl`. Published on SourceForge as `xsltml_2.1.2.zip`. |

No release after 2.1.2 has been made. The author confirmed end of maintenance in January 2011.

## Current mirrors

Because the original host is gone and SourceForge's long-term reliability is uncertain, several mirrors of the final 2.1.2 release now exist. The ones known to be faithful to the upstream bytes include:

- SourceForge: <https://sourceforge.net/projects/xsltml/>
- This repository: <https://github.com/stultus/mathml2tex> (under `mathml2tex/xsl_yarosh/`)
- GitLab (XCDS import, 2021): <https://gitlab.com/xcds/xslt-mathml-library>
- Embedded inside OERPUB's `mathconverter`: <https://github.com/oerpub/mathconverter>

## Why this document exists in this repository

This repository uses `xsl_yarosh` as its MathML-to-LaTeX conversion engine. Because the stylesheets reference a URL that no longer exists, and because the name "Vasil Yaroshevich" is unfamiliar to most contemporary readers, this document is included so that future maintainers and users can:

1. Understand what `xsl_yarosh` is and where it came from.
2. Verify that the code carries a permissive licence from its original author.
3. Trace lineage if they encounter the same headers in other projects.
4. Preserve attribution to the original author in accordance with the licence, even after the upstream site has disappeared.

---

*Last updated: April 2026.*
