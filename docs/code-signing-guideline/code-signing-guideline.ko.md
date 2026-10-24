# macOS 코드 서명 가이드

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](code-signing-guideline.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/flat.svg)](code-signing-guideline.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](code-signing-guideline.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](code-signing-guideline.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](code-signing-guideline.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](code-signing-guideline.fr.md)

코드 서명(Code Signing)은 macOS가 애플리케이션을 만든 주체와, 서명 이후 변경되지 않았음을 확인하게 해 줍니다. Mac App Store 외부로 배포하는 소프트웨어는 Apple Developer Program에서 발급받은 **Developer ID Application** 인증서로 서명합니다.

## 서명과 공증은 별개의 단계입니다

- **서명**(`codesign`)은 코드에 Developer ID 서명을 붙입니다. 코드의 출처와 무결성을 증명합니다.
- **공증**(`notarytool`)은 서명된 빌드를 Apple에 업로드하면 Apple이 자동 검사 후 티켓을 발급합니다. Gatekeeper 기본 정책에서는 App Store 외부로 배포되는 Developer ID 서명 소프트웨어가 공증되어야 하며, 이는 macOS 10.15 (Catalina)부터 2019년 6월 이후 빌드된 소프트웨어에 적용됩니다.
- 공증에는 앱과 명령줄 타깃에 하드닝된 런타임(`--options runtime`)을 활성화하고, 각 서명에 보안 타임스탬프(`--timestamp`)를 적용해야 합니다.

## 사전 준비

- Apple Developer Program에 가입하고 **Developer ID Application** 인증서를 생성합니다. 서명하는 Mac의 키체인(예: 로그인 키체인)에 개인 키와 함께 보관합니다.
- `notarytool`과 `stapler`가 포함된 지원되는 Xcode를 설치하고 해당 개발자 도구를 선택합니다(예: `sudo xcode-select -s "/Applications/Xcode.app"`). `codesign`과 `spctl`은 macOS에 기본 포함되어 있습니다.
- 직접 만들었거나 신뢰하는 빌드만 서명합니다. 서명이 신뢰할 수 없는 코드를 안전하게 만들지는 않습니다.
- 서명에 iCloud 로그인은 필요하지 않습니다.

## 안쪽부터 바깥쪽으로 서명

중첩된 코드(dylib, 프레임워크, 헬퍼, XPC 서비스, 플러그인)를 먼저 서명하고 바깥쪽 번들을 마지막에 서명해야 각 서명이 이미 서명된 내용을 포함합니다. 서명에 `--deep`을 사용하지 마십시오. 모든 항목에 동일한 옵션을 적용하며 Apple도 서명용으로는 권장하지 않습니다. 앱에 권한(entitlements)이 필요한 경우에만 `--entitlements "[FILE].entitlements"`를 추가합니다.

```bash
# Developer ID Application identity (list available identities with: security find-identity -v -p codesigning)
IDENTITY="Developer ID Application: [NAME] ([TEAM_ID])"

# 1) 중첩 코드 먼저
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[LIB].dylib"
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[NAME].framework"

# 2) 바깥쪽 앱 번들은 마지막
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app"
```

불필요한 메타데이터(리소스 포크, Finder 파일 등) 때문에 서명이 실패하면 빌드 산출물을 정리하거나 `ditto --norsrc --noextattr`처럼 깨끗하게 복사하십시오. 모든 파일의 확장 속성을 기본적으로 삭제하지 마십시오.

## 서명 검증

`codesign`으로 검증한 뒤 `spctl`로 Gatekeeper 평가를 확인합니다. 공증 전에는 `spctl`이 공증되지 않은 앱으로 거부할 수 있으며 정상입니다.

```bash
codesign --verify --deep --strict --verbose=2 "[APP].app"
codesign --display --verbose=4 "[APP].app"
spctl --assess --type execute --verbose=4 "[APP].app"
```

## 공증 및 스테이플

단독 `.dylib`이 아니라 서명된 앱의 압축본(`.zip`, `.dmg`, `.pkg`)을 제출합니다. 승인되면 티켓을 스테이플하고 위 검증을 다시 실행합니다.

```bash
# One-time: store notarization credentials in the keychain (prompts for an app-specific password)
xcrun notarytool store-credentials "[PROFILE]" --apple-id "[APPLE_ID]" --team-id "[TEAM_ID]"

ditto -c -k --keepParent "[APP].app" "[APP].zip"
xcrun notarytool submit "[APP].zip" --keychain-profile "[PROFILE]" --wait
xcrun stapler staple "[APP].app"
xcrun stapler validate "[APP].app"
```

## 레퍼런스

- <https://developer.apple.com/support/code-signing/>
- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- <https://developer.apple.com/documentation/security/customizing-the-notarization-workflow>
- <https://developer.apple.com/documentation/security/resolving-common-notarization-issues>
- <https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web>
- <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web>
