# Hướng dẫn ký mã (code signing) trên macOS

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](code-signing-guideline.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](code-signing-guideline.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](code-signing-guideline.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/flat.svg)](code-signing-guideline.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](code-signing-guideline.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](code-signing-guideline.fr.md)

Ký mã cho phép macOS xác minh ai đã tạo ra ứng dụng và ứng dụng chưa bị thay đổi kể từ khi được ký. Phần mềm phân phối ngoài Mac App Store được ký bằng chứng chỉ **Developer ID Application** do Apple Developer Program cấp.

## Ký và công chứng (notarization) là hai bước khác nhau

- **Ký** (`codesign`) gắn chữ ký Developer ID của bạn vào mã, chứng minh nguồn gốc và tính toàn vẹn của mã.
- **Công chứng** (`notarytool`) tải bản build đã ký lên Apple; Apple quét tự động rồi cấp một ticket. Theo chính sách mặc định của Gatekeeper, phần mềm ký bằng Developer ID và phân phối ngoài App Store được kỳ vọng phải được công chứng; điều này áp dụng từ macOS 10.15 (Catalina) cho phần mềm build sau tháng 6/2019.
- Công chứng yêu cầu bật Hardened Runtime (`--options runtime`) cho các target ứng dụng và dòng lệnh, cùng dấu thời gian an toàn (`--timestamp`) trên mỗi chữ ký.

## Điều kiện tiên quyết

- Đăng ký Apple Developer Program và tạo chứng chỉ **Developer ID Application**. Lưu chứng chỉ cùng khóa riêng trong keychain của máy Mac thực hiện việc ký (ví dụ keychain đăng nhập).
- Cài đặt phiên bản Xcode được hỗ trợ (đã bao gồm `notarytool` và `stapler`) và chọn bộ công cụ phát triển của nó (ví dụ `sudo xcode-select -s "/Applications/Xcode.app"`). `codesign` và `spctl` có sẵn trong macOS.
- Chỉ ký các bản build do bạn tạo ra hoặc đáng tin cậy. Việc ký không làm cho mã không đáng tin trở nên an toàn.
- Ký mã không yêu cầu đăng nhập iCloud.

## Ký từ trong ra ngoài

Ký mã lồng bên trong trước (dylib, framework, helper, dịch vụ XPC, plug-in), rồi ký bundle ngoài cùng sau cùng để mỗi chữ ký bao phủ nội dung đã được ký. Không dùng `--deep` để ký: tùy chọn này áp dụng cùng một bộ tùy chọn cho mọi thứ và Apple không khuyến nghị dùng để ký. Chỉ thêm `--entitlements "[FILE].entitlements"` khi ứng dụng cần entitlements.

```bash
# Developer ID Application identity (list available identities with: security find-identity -v -p codesigning)
IDENTITY="Developer ID Application: [NAME] ([TEAM_ID])"

# 1) Mã lồng bên trong trước
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[LIB].dylib"
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[NAME].framework"

# 2) Bundle ứng dụng ngoài cùng sau cùng
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app"
```

Nếu việc ký thất bại do siêu dữ liệu thừa (ví dụ resource fork hoặc tệp Finder), hãy sửa đầu ra của bản build hoặc sao chép sạch, ví dụ `ditto --norsrc --noextattr`. Không xóa thuộc tính mở rộng của mọi tệp một cách mặc định.

## Xác minh chữ ký

Xác minh bằng `codesign`, rồi hỏi Gatekeeper bằng `spctl`. Trước khi công chứng, `spctl` có thể từ chối ứng dụng vì chưa được công chứng; điều này là bình thường.

```bash
codesign --verify --deep --strict --verbose=2 "[APP].app"
codesign --display --verbose=4 "[APP].app"
spctl --assess --type execute --verbose=4 "[APP].app"
```

## Công chứng và staple

Gửi tệp lưu trữ (`.zip`, `.dmg` hoặc `.pkg`) của ứng dụng đã ký, không gửi riêng một `.dylib`. Sau khi được chấp nhận, staple ticket và chạy lại bước xác minh ở trên.

```bash
# One-time: store notarization credentials in the keychain (prompts for an app-specific password)
xcrun notarytool store-credentials "[PROFILE]" --apple-id "[APPLE_ID]" --team-id "[TEAM_ID]"

ditto -c -k --keepParent "[APP].app" "[APP].zip"
xcrun notarytool submit "[APP].zip" --keychain-profile "[PROFILE]" --wait
xcrun stapler staple "[APP].app"
xcrun stapler validate "[APP].app"
```

## Tài liệu tham khảo

- <https://developer.apple.com/support/code-signing/>
- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- <https://developer.apple.com/documentation/security/customizing-the-notarization-workflow>
- <https://developer.apple.com/documentation/security/resolving-common-notarization-issues>
- <https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web>
- <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web>
