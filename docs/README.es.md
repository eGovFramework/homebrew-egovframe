# homebrew-egovframe

<!-- latest-badge:start -->
[![Marco Estándar de Gobierno Electrónico 5.0.2](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/5.0.2/flat-es.svg)](https://www.egovframe.go.kr/)
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../LICENSE)
<!-- latest-badge:end -->

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](README.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](README.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/flat.svg)](README.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](README.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](README.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](README.fr.md)

## Acerca de

Casks de Homebrew para el entorno de desarrollo integrado (IDE) de eGovFrame en macOS. Los paquetes se descargan directamente desde el servidor oficial de eGovFrame.

- [Sitio web oficial de eGovFrame](https://www.egovframe.go.kr/)
- [Descargas del entorno de desarrollo](https://www.egovframe.go.kr/home/sub.do?menuNo=40)
- [Guía de firma de código](code-signing-guideline/code-signing-guideline.es.md)

## Instalación

### Agregar el tap oficial

Instale primero [Homebrew](https://brew.sh/) y luego registre este tap una sola vez:

```bash
brew tap egovframework/egovframe
```

### Instalar la versión más reciente

```bash
brew install --cask egovframework/egovframe/egovframedev-latest
```

El cask de la última versión se llama `egovframedev-latest`. Utilice ese nombre explícitamente.

### Instalar una versión específica

Elija uno de los casks disponibles:

```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

Si otro tap incluye un cask con el mismo nombre, especifique el nombre completo `egovframework/egovframe/egovframedev@<version>`.

### Actualizar el cask más reciente

```bash
brew update
brew upgrade --cask egovframework/egovframe/egovframedev-latest
```

## Arquitecturas compatibles y ruta de la aplicación

- Todos los casks listados excepto 3.10.0 y 4.0.0 ofrecen binarios para Apple Silicon (ARM64) e Intel (x86_64); Homebrew selecciona automáticamente la arquitectura correspondiente.
- Las versiones 3.10.0 y 4.0.0 ofrecen únicamente binarios Intel (x86_64).
- Las aplicaciones se instalan en `/Applications/`:
  - 3.10.0 y 4.0.0: `eGovFrameDev-X.X.X-Mac-64bit.app`
  - Casks de doble arquitectura con nomenclatura `Mac`: `eGovFrameDev-X.X.X-Mac-AArch64.app` o `eGovFrameDev-X.X.X-Mac-x86_64.app`
  - Casks de doble arquitectura con nomenclatura `macOS`: `eGovFrameDev-X.X.X-macOS-AArch64.app` o `eGovFrameDev-X.X.X-macOS-x86_64.app`

## Licencia

Consulte [LICENSE](../LICENSE). Los nombres y logotipos de eGovFrame pertenecen a sus respectivos titulares.
