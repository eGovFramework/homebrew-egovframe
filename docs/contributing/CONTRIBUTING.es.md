# Guía de contribución

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/flat.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](CONTRIBUTING.fr.md)

## Antes de abrir un pull request

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # pruebas de los scripts
brew style egovframework/egovframe/egovframedev-latest   # requiere el tap: brew tap egovframework/egovframe
```

El CI (`ci.yml`) ejecuta las pruebas y además `scripts/check_tap.sh` (`brew readall`, `brew style` y `brew audit`). Ejecuta los comandos desde la raíz del repositorio; las pruebas de los scripts necesitan PyYAML, que el CI instala del mismo modo.

- Los mensajes de commit siguen el estilo que ya se usa en el repositorio oficial: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- No edites a mano el SHA-256 de un cask. Las versiones nuevas salen de `scripts/update_casks.py` (el flujo de trabajo `Update casks`); para volver a comprobar un hash existente ejecuta `gh workflow run update-casks.yml -f verify=<version>`.
- Un cask por serie menor: al añadir `5.0.3` se elimina `5.0.2` (misma convención que en el repositorio oficial).

## GitHub Actions y facturación

- **Gratis en repositorios públicos:** según la política de facturación de GitHub, los runners estándar alojados por GitHub (`ubuntu-latest`, `macos-latest`) son **gratuitos y sin límite de minutos en repositorios públicos**. Los DMG se procesan para calcular su hash en flujo durante `update-casks.yml` y nunca se suben como artefactos de Actions ni como recursos de Release, por lo que tampoco se consume cuota de almacenamiento de Actions.
- Los minutos solo se descuentan de la cuota gratuita de tu cuenta si copias el repositorio a uno privado y lo ejecutas allí.

## Seguridad

No notifiques vulnerabilidades en issues; sigue el proceso descrito en [SECURITY.es.md](../security/SECURITY.es.md).
