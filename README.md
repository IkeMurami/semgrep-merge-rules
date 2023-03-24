# Semgrep merge rules

The Semgrep can scan over rule presets or over a rule (rules folders). If we want to use rules from different presets we should copy them or use a preset in full (and good rules and bad rules). It isn't convinient.

That script is based on [merge-rules.py](https://github.com/returntocorp/semgrep/blob/develop/scripts/merge-rules.py) from semgrep. We get rules from different sources and combine to one big rule.

# Usage

Run:

```
$ poetry config virtualenvs.in-project true
$ poetry install
$ poetry run python -B main.py --help
$ poetry run python -B src/main.py test/test* https://storage.yandexcloud.net/semgrep-rules/presets/test2.yaml
```

Example of preset.yaml:

```yaml
# Description: 
# That preset scans PHP code.
---
preset:
  - path: /Users/ikemurami/Work/Tools/appsec/semgrep-rules/dockerfile/best-practice/avoid-apk-upgrade.yaml
    ids:
      - avoid-apk-upgrade
  - path: /Users/ikemurami/Work/Tools/appsec/semgrep-rules/contrib/dlint/dlint-equivalent.yaml
    ids:
      - insecure-eval-use
      - insecure-xml-use
      - insecure-dl-use
  - url: https://raw.githubusercontent.com/returntocorp/semgrep-rules/develop/generic/secrets/security/detected-artifactory-token.yaml
    ids:
      - detected-artifactory-token
```