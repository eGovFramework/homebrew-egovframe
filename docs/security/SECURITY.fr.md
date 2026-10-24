# Politique de sécurité

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](SECURITY.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](SECURITY.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](SECURITY.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](SECURITY.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](SECURITY.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/flat.svg)](SECURITY.fr.md)

## Signaler une vulnérabilité

**N'ouvrez pas de ticket public pour un problème de sécurité.**

Utilisez plutôt le signalement privé de vulnérabilités de GitHub :

➡ <https://github.com/eGovFramework/homebrew-egovframe/security/advisories/new>

Si le signalement privé de vulnérabilités n'est pas activé sur le dépôt, signalez le problème via le [portail officiel eGovFrame](https://www.egovframe.go.kr/) au lieu d'ouvrir un ticket public.

Merci d'indiquer :

- ce qui est concerné (nom et version du cask, workflow ou script)
- comment reproduire le problème et l'impact attendu
- ce que vous avez déjà fait pour le vérifier (hashes, URL, journaux)

Les signalements sont traités de manière privée jusqu'à la disponibilité d'un correctif ; vous êtes crédité sur demande.

## Périmètre

Dans le périmètre :

- Les casks de [`Casks/`](../../Casks) : URL de téléchargement, valeurs SHA-256 et scripts d'installation. L'ancien cask `egovframedev@4.2.1` exécute un `postflight` qui télécharge une icône avec `curl` et supprime l'attribut de quarantaine de macOS ; signalez tout ce qui rend cela dangereux.
- L'automatisation : [`.github/workflows/`](../../.github/workflows) et [`scripts/`](../../scripts). Les nouveaux casks sont générés en téléchargeant les DMG officiels et en calculant leur hash en CI ; tout moyen de faire produire un hash erroné à cette étape, de divulguer le jeton ou d'exécuter une entrée non fiable est une vulnérabilité.

Hors périmètre, à signaler au responsable :

- L'IDE eGovFrame et son serveur de téléchargement → le projet eGovFrame, <https://www.egovframe.go.kr/> et [eGovFramework](https://github.com/eGovFramework).
- Homebrew lui-même → <https://github.com/Homebrew/brew/security/policy>.
## Versions prises en charge

Seul ce qui se trouve dans `Casks/` sur la branche par défaut (`main`) est maintenu : `egovframedev-latest` et les casks versionnés listés dans le [README](../README.fr.md). Les casks supprimés à l'arrivée d'un correctif plus récent de la même série ne le sont pas.

## Vérifier un téléchargement vous-même

Chaque cask fige un SHA-256 pour chaque architecture qu'il fournit, et chaque [Release](https://github.com/eGovFramework/homebrew-egovframe/releases) les liste. Certains casks versionnés (par exemple 3.10.0 et 4.0.0) sont réservés à Intel et ne figent donc qu'un seul hash. Pour revérifier une version auprès du serveur officiel depuis la CI :

```bash
gh workflow run update-casks.yml -R eGovFramework/homebrew-egovframe -f verify=5.0.2
```
