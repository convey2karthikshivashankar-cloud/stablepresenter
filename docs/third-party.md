# Third-party components

The application source is MIT licensed. Install required tools and dependencies from their upstream distributions. Their licenses remain applicable; they are not relicensed by the application.

- Quarto CLI and bundled publishing tools: https://github.com/quarto-dev/quarto-cli
- JSON Schema validator: https://github.com/python-jsonschema/jsonschema
- PyYAML safe YAML parser: https://github.com/yaml/pyyaml
- Playwright browser automation: https://github.com/microsoft/playwright-python
- pytest: https://github.com/pytest-dev/pytest
- Pillow image comparison: https://github.com/python-pillow/Pillow
- Python build frontend: https://github.com/pypa/build
- Bootstrap, included by Quarto in generated HTML: https://github.com/twbs/bootstrap

Generated reports retain Quarto's embedded asset notices. No external fonts, remote scripts or paid APIs are required to view the generated report. The source archive contains the application wheel and source distribution; it excludes Quarto, Chromium, virtual environments and third-party Python package binaries.
