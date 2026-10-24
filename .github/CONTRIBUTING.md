# Contributing

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/flat.svg)](/docs/contributing/CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](/docs/contributing/CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](/docs/contributing/CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](/docs/contributing/CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](/docs/contributing/CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](/docs/contributing/CONTRIBUTING.fr.md)

## Before you open a pull request

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # script tests
brew style egovframework/egovframe/egovframedev-latest   # needs the tap: brew tap egovframework/egovframe
```

CI (`ci.yml`) runs the tests plus `scripts/check_tap.sh` (`brew readall`, `brew style` and `brew audit`). Run the commands from the repository root; the script tests need PyYAML, which CI installs the same way.

- Commit messages follow the style already used upstream: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- Do not edit the SHA-256 of a cask by hand. New versions come from `scripts/update_casks.py` (the `Update casks` workflow); to re-check an existing hash run `gh workflow run update-casks.yml -f verify=<version>`.
- One cask per minor series: when `5.0.3` is added, `5.0.2` is removed (same convention as upstream).

## GitHub Actions & Billing

- **Free on public repositories:** Standard GitHub-hosted runners (`ubuntu-latest`, `macos-latest`) are **free without minute limits on public repositories** under GitHub's billing policy. DMGs are hashed in-stream during `update-casks.yml` and are never uploaded as Actions artifacts or Release assets, so no Actions storage quota is consumed either.
- Minutes are deducted from your account's free allowance only if you copy the repository into a private repository and run it there.

## Security

Do not report vulnerabilities in issues; follow the process in [SECURITY.en.md](/docs/security/SECURITY.en.md).
