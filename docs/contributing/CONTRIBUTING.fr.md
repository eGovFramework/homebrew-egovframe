# Contribuer

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/flat.svg)](CONTRIBUTING.fr.md)

## Avant d'ouvrir une pull request

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # tests des scripts
brew style egovframework/egovframe/egovframedev-latest   # nécessite le tap : brew tap egovframework/egovframe
```

La CI (`ci.yml`) exécute les tests ainsi que `scripts/check_tap.sh` (`brew readall`, `brew style` et `brew audit`). Lancez les commandes depuis la racine du dépôt ; les tests des scripts ont besoin de PyYAML, que la CI installe de la même façon.

- Les messages de commit suivent le style déjà utilisé dans le dépôt officiel : `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- Ne modifiez pas à la main le SHA-256 d'un cask. Les nouvelles versions proviennent de `scripts/update_casks.py` (le workflow `Update casks`) ; pour revérifier un hash existant, exécutez `gh workflow run update-casks.yml -f verify=<version>`.
- Un seul cask par série mineure : lorsque `5.0.3` est ajouté, `5.0.2` est supprimé (même convention que le dépôt officiel).

## GitHub Actions et facturation

- **Gratuit sur les dépôts publics :** selon la politique de facturation de GitHub, les runners standard hébergés par GitHub (`ubuntu-latest`, `macos-latest`) sont **gratuits et sans limite de minutes sur les dépôts publics**. Les DMG sont hachés au fil du flux pendant `update-casks.yml` et ne sont jamais téléversés comme artefacts Actions ni comme ressources de Release ; aucun quota de stockage Actions n'est donc consommé.
- Les minutes ne sont décomptées du quota gratuit de votre compte que si vous copiez le dépôt vers un dépôt privé et l'y exécutez.

## Sécurité

Ne signalez pas de vulnérabilités dans les issues ; suivez la procédure décrite dans [SECURITY.fr.md](../security/SECURITY.fr.md).
