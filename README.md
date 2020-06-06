# Proviola

[![Contributing][contributing-shield]][contributing-link]
[![Code of Conduct][conduct-shield]][conduct-link]
[![Zulip][zulip-shield]][zulip-link]


[contributing-shield]: https://img.shields.io/badge/contributions-welcome-%23f7931e.svg
[contributing-link]: https://github.com/coq-community/manifesto/blob/master/CONTRIBUTING.md

[conduct-shield]: https://img.shields.io/badge/%E2%9D%A4-code%20of%20conduct-%23f15a24.svg
[conduct-link]: https://github.com/coq-community/manifesto/blob/master/CODE_OF_CONDUCT.md

[zulip-shield]: https://img.shields.io/badge/chat-on%20zulip-%23c1272d.svg
[zulip-link]: https://coq.zulipchat.com/#narrow/stream/237663-coq-community-devs.20.26.20users



Proviola is a tool for creating "proof movies" out of proof scripts,
in particular, scripts for the Coq and Isabelle proof assistants,
and transforming these movies into "dynamic" HTML pages.

## Meta

- Author(s):
  - Carst Tankink (initial)
- Coq-community maintainer(s):
  - Jason Gross ([**@JasonGross**](https://github.com/JasonGross))
- License: [GNU General Public License v3.0 or later](LICENSE)
- Additional dependencies:
  - [lxml library](https://lxml.de)
- Related publication(s):
  - [Proviola: a Tool for Proof Re-animation](https://arxiv.org/abs/1005.2672) doi:[10.1007/978-3-642-14128-7_37](https://doi.org/10.1007/978-3-642-14128-7_37)

## Usage

Run coqdoc on your sources, then run the `camera.py` script on the generated HTML file. Optionally provide an output file.
On the generated xml file (default extension: .flm), run an XSL processor such as xsltproc (linux) to get an HTML page.
The default XSL template is proviola/coq/proviola.xsl, which includes the required JavaScript and CSS.

There is a known bug in processing "plain" scripts, not pre-processed by coqdoc.


