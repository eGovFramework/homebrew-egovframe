# 기여 안내

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/flat.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](CONTRIBUTING.fr.md)

## 풀 리퀘스트를 열기 전에

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # 스크립트 테스트
brew style egovframework/egovframe/egovframedev-latest   # 탭이 필요합니다: brew tap egovframework/egovframe
```

CI(`ci.yml`)는 테스트와 함께 `scripts/check_tap.sh`(`brew readall`, `brew style`, `brew audit`)를 실행합니다. 명령은 저장소 루트에서 실행하세요. 스크립트 테스트에는 PyYAML이 필요하며 CI도 같은 방식으로 설치합니다.

- 커밋 메시지는 업스트림에서 이미 쓰는 형식을 따릅니다: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- cask의 SHA-256 은 직접 수정하지 마세요. 새 버전은 `scripts/update_casks.py`(`Update casks` 워크플로)로 만들어지며, 기존 해시를 다시 확인하려면 `gh workflow run update-casks.yml -f verify=<version>` 을 실행하세요.
- 마이너 시리즈당 cask 하나: `5.0.3` 을 추가하면 `5.0.2` 는 제거합니다(업스트림과 같은 규칙).

## GitHub Actions 및 비용

- **공개 저장소는 무료:** GitHub의 요금 정책에 따라 공개 저장소에서는 표준 GitHub 호스팅 러너(`ubuntu-latest`, `macos-latest`)를 **분 제한 없이 무료**로 사용할 수 있습니다. DMG 파일은 `update-casks.yml` 실행 중 스트림으로 해시만 계산하며 Actions 아티팩트나 Release 자산으로 업로드하지 않으므로 Actions 스토리지 할당량도 사용하지 않습니다.
- 저장소를 비공개 저장소로 복제해 실행하는 경우에만 계정의 무료 제공량에서 사용 시간이 차감됩니다.

## 보안

취약점은 이슈로 신고하지 말고 [SECURITY.ko.md](../security/SECURITY.ko.md) 의 절차를 따라 알려 주세요.
