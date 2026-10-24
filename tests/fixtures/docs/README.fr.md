# homebrew-egovframe

<!-- latest-badge:start -->
[![Cadre standard de l'administration électronique](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/unversioned/flat-fr.svg)](https://www.egovframe.go.kr/)
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../LICENSE)
<!-- latest-badge:end -->

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](README.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](README.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](README.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](README.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](README.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/flat.svg)](README.fr.md)

## À propos

Casks Homebrew pour l'environnement de développement intégré (IDE) eGovFrame sur macOS. Les archives sont téléchargées directement depuis le serveur officiel d'eGovFrame.

- [Site officiel d'eGovFrame](https://www.egovframe.go.kr/)
- [Téléchargements de l'environnement de développement](https://www.egovframe.go.kr/home/sub.do?menuNo=40)
- [Guide de signature de code](code-signing-guideline/code-signing-guideline.fr.md)

## Installation

### Ajouter le tap officiel

Installez d'abord [Homebrew](https://brew.sh/), puis ajoutez ce tap une seule fois :

```bash
brew tap egovframework/egovframe
```

### Installer la dernière version

```bash
brew install --cask egovframework/egovframe/egovframedev-latest
```

Le cask de la dernière version dans ce tap se nomme `egovframedev-latest`. Utilisez explicitement ce nom lors de l'installation.

### Installer une version spécifique

Choisissez l'un des casks disponibles :

```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

Si un autre tap fournit un cask portant le même nom, utilisez le nom complet `egovframework/egovframe/egovframedev@<version>`.

### Mettre à jour le dernier cask

```bash
brew update
brew upgrade --cask egovframework/egovframe/egovframedev-latest
```

## Architectures prises en charge et chemin de l'application

- Tous les casks listés à l'exception des versions 3.10.0 et 4.0.0 fournissent des binaires pour Apple Silicon (ARM64) et Intel (x86_64) ; Homebrew sélectionne automatiquement l'architecture correspondante.
- Les versions 3.10.0 et 4.0.0 fournissent uniquement des binaires Intel (x86_64).
- Les applications sont installées dans `/Applications/` :
  - 3.10.0 et 4.0.0 : `eGovFrameDev-X.X.X-Mac-64bit.app`
  - Casks bi-architecture utilisant la nomenclature `Mac` : `eGovFrameDev-X.X.X-Mac-AArch64.app` ou `eGovFrameDev-X.X.X-Mac-x86_64.app`
  - Casks bi-architecture utilisant la nomenclature `macOS` : `eGovFrameDev-X.X.X-macOS-AArch64.app` ou `eGovFrameDev-X.X.X-macOS-x86_64.app`

## Licence

Voir [LICENSE](../LICENSE). Les noms et logos d'eGovFrame appartiennent à leurs détenteurs respectifs.
