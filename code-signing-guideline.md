# macOS Code Signing Guide

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/flat.svg)](docs/code-signing-guideline/code-signing-guideline.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](docs/code-signing-guideline/code-signing-guideline.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](docs/code-signing-guideline/code-signing-guideline.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](docs/code-signing-guideline/code-signing-guideline.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](docs/code-signing-guideline/code-signing-guideline.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](docs/code-signing-guideline/code-signing-guideline.fr.md)

Code signing lets macOS verify who built an application and that it has not been modified since it was signed. Software distributed outside the Mac App Store is signed with a **Developer ID Application** certificate issued through the Apple Developer Program.

## Signing and notarization are different steps

- **Signing** (`codesign`) attaches your Developer ID signature to the code. It proves the origin and integrity of the code.
- **Notarization** (`notarytool`) uploads the signed build to Apple, which scans it automatically and issues a ticket. Under Gatekeeper's default policy, Developer ID-signed software distributed outside the App Store is expected to be notarized; this has applied since macOS 10.15 (Catalina) to software built after June 2019.
- Notarization requires enabling the Hardened Runtime (`--options runtime`) for app and command-line targets, and a secure timestamp (`--timestamp`) on each signature.

## Prerequisites

- Enroll in the Apple Developer Program and create a **Developer ID Application** certificate. Keep it, with its private key, in the keychain of the Mac that signs (for example the login keychain).
- Install a supported version of Xcode, which includes `notarytool` and `stapler`, and select its developer tools (for example `sudo xcode-select -s "/Applications/Xcode.app"`). `codesign` and `spctl` ship with macOS.
- Sign only builds that you own or trust. Signing does not make untrusted code safe.
- Signing does not require being signed in to iCloud.

## Sign the code, inside out

Sign nested code first (dylibs, frameworks, helpers, XPC services, plug-ins), then the outer bundle last, so each signature covers already-signed contents. Do not rely on `--deep` to sign: it applies one set of options to everything and Apple discourages it for signing. Add `--entitlements "[FILE].entitlements"` only if the app needs entitlements.

```bash
# Developer ID Application identity (list available identities with: security find-identity -v -p codesigning)
IDENTITY="Developer ID Application: [NAME] ([TEAM_ID])"

# 1) Nested code first
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[LIB].dylib"
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[NAME].framework"

# 2) Outer app bundle last
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app"
```

If signing fails because of stray metadata (for example resource forks or Finder files), fix the build output or copy it cleanly, for example `ditto --norsrc --noextattr`. Do not strip extended attributes from every file by default.

## Verify the signature

Verify with `codesign`, then ask Gatekeeper with `spctl`. Before notarization, `spctl` may reject the app as unnotarized; that is expected.

```bash
codesign --verify --deep --strict --verbose=2 "[APP].app"
codesign --display --verbose=4 "[APP].app"
spctl --assess --type execute --verbose=4 "[APP].app"
```

## Notarize and staple

Submit an archive (`.zip`, `.dmg` or `.pkg`) of the signed app, not a bare `.dylib`. After it is accepted, staple the ticket and re-run the verification above.

```bash
# One-time: store notarization credentials in the keychain (prompts for an app-specific password)
xcrun notarytool store-credentials "[PROFILE]" --apple-id "[APPLE_ID]" --team-id "[TEAM_ID]"

ditto -c -k --keepParent "[APP].app" "[APP].zip"
xcrun notarytool submit "[APP].zip" --keychain-profile "[PROFILE]" --wait
xcrun stapler staple "[APP].app"
xcrun stapler validate "[APP].app"
```

## References

- <https://developer.apple.com/support/code-signing/>
- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- <https://developer.apple.com/documentation/security/customizing-the-notarization-workflow>
- <https://developer.apple.com/documentation/security/resolving-common-notarization-issues>
- <https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web>
- <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web>
