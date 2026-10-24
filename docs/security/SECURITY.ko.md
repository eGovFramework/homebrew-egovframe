# 보안 정책

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](SECURITY.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/flat.svg)](SECURITY.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](SECURITY.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](SECURITY.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](SECURITY.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](SECURITY.fr.md)

## 취약점 접수

**보안 문제는 공개 이슈로 올리지 말아 주세요.**

대신 GitHub 비공개 취약점 신고를 이용해 주세요.

➡ <https://github.com/eGovFramework/homebrew-egovframe/security/advisories/new>

저장소에 비공개 취약점 신고가 활성화되어 있지 않다면, 공개 이슈 대신 공식 [표준프레임워크 포털](https://www.egovframe.go.kr/)을 통해 접수해 주세요.

다음을 포함해 주세요.

- 영향받는 대상 (cask 이름·버전, 워크플로, 스크립트)
- 재현 방법과 예상되는 영향
- 이미 확인한 내용 (해시, URL, 로그)

수정이 나올 때까지 비공개로 처리하며, 원하시면 제보자로 표기합니다.

## 범위

대상:

- [`Casks/`](../../Casks)의 cask: 다운로드 URL, SHA-256, 설치 스크립트. 옛 cask `egovframedev@4.2.1`의 `postflight`는 `curl`로 아이콘을 받고 macOS 격리 속성을 제거합니다. 이것이 안전하지 않게 되는 경우를 알려 주세요.
- 자동화: [`.github/workflows/`](../../.github/workflows)와 [`scripts/`](../../scripts). 새 cask는 CI가 공식 DMG를 받아 해시를 계산해 만듭니다. 이 과정에서 잘못된 해시가 들어가거나, 토큰이 노출되거나, 신뢰할 수 없는 입력이 실행되는 경우는 취약점입니다.

범위 밖 (해당 주체에 알려 주세요):

- eGovFrame IDE와 배포 서버 → 표준프레임워크 프로젝트, <https://www.egovframe.go.kr/> 및 [eGovFramework](https://github.com/eGovFramework).
- Homebrew 자체 → <https://github.com/Homebrew/brew/security/policy>.
## 지원 대상

기본 브랜치(`main`)의 `Casks/`에 있는 것만 관리합니다. `egovframedev-latest`와 [README](../README.ko.md)에 나열된 버전별 cask가 해당합니다. 같은 계열의 새 패치가 나와 삭제된 cask는 대상이 아닙니다.

## 직접 해시 확인

모든 cask는 제공하는 각 아키텍처의 SHA-256을 고정하며, [Release](https://github.com/eGovFramework/homebrew-egovframe/releases)에도 적혀 있습니다. 일부 버전별 cask(예: 3.10.0, 4.0.0)는 Intel 전용이라 해시가 하나뿐입니다. CI에서 공식 서버와 다시 대조하려면:

```bash
gh workflow run update-casks.yml -R eGovFramework/homebrew-egovframe -f verify=5.0.2
```
