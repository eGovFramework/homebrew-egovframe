# homebrew-egovframe

<!-- latest-badge:start -->
[![전자정부표준프레임워크 5.0.2](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/5.0.2/flat-ko.svg)](https://www.egovframe.go.kr/)
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../LICENSE)
<!-- latest-badge:end -->

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](README.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/flat.svg)](README.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](README.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](README.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](README.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](README.fr.md)

## 소개

macOS용 전자정부 표준프레임워크 개발환경(IDE)을 설치하는 Homebrew tap입니다. 설치 파일은 표준프레임워크 공식 서버에서 내려받습니다.

- [표준프레임워크 포털](https://www.egovframe.go.kr/)
- [개발환경 다운로드](https://www.egovframe.go.kr/home/sub.do?menuNo=40)
- [코드 서명 가이드](code-signing-guideline/code-signing-guideline.ko.md)

## 설치 방법

### 공식 tap 추가

[Homebrew](https://brew.sh/)를 설치한 뒤 최초 한 번 실행합니다.

```bash
brew tap egovframework/egovframe
```

### 최신 버전 설치

```bash
brew install --cask egovframework/egovframe/egovframedev-latest
```

이 tap의 최신 버전 cask 이름은 `egovframedev-latest`입니다. 버전별 cask에서 버전 번호를 생략하는 방식이 아니라, 위 이름을 명시해 설치합니다.

### 특정 버전 설치

필요한 버전의 명령 하나를 선택해 실행합니다.

```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

위 명령은 공식 tap을 추가한 상태를 기준으로 합니다. 다른 tap에도 같은 이름의 cask가 있다면 `egovframework/egovframe/egovframedev@<버전>` 형식으로 원하는 버전의 전체 이름을 지정하세요.

### 최신 cask 업데이트

```bash
brew update
brew upgrade --cask egovframework/egovframe/egovframedev-latest
```

## 지원 아키텍처와 앱 설치 경로

- 위 목록에서 3.10.0·4.0.0을 제외한 cask는 Apple Silicon(ARM64)과 Intel(x86_64)용 설치 파일을 제공합니다. Homebrew가 아키텍처에 맞는 파일을 선택합니다.
- 3.10.0·4.0.0은 Intel(x86_64)용 설치 파일만 제공하며 Apple Silicon 네이티브 빌드는 아닙니다.
- 앱은 `/Applications/` 아래에 설치됩니다.
  - 3.10.0·4.0.0: `eGovFrameDev-X.X.X-Mac-64bit.app`
  - 기존 `Mac` 이름을 사용하는 이중 아키텍처 cask: `eGovFrameDev-X.X.X-Mac-AArch64.app` 또는 `eGovFrameDev-X.X.X-Mac-x86_64.app`
  - 새 `macOS` 이름을 사용하는 이중 아키텍처 cask: `eGovFrameDev-X.X.X-macOS-AArch64.app` 또는 `eGovFrameDev-X.X.X-macOS-x86_64.app`

## 라이선스

[LICENSE](../LICENSE)를 참고하세요. eGovFrame 명칭과 로고의 권리는 각 권리자에게 있습니다.
