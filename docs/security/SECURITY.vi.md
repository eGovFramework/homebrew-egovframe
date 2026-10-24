# Chính sách bảo mật

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](SECURITY.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](SECURITY.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](SECURITY.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/flat.svg)](SECURITY.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](SECURITY.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](SECURITY.fr.md)

## Báo cáo lỗ hổng

**Vui lòng không mở issue công khai cho vấn đề bảo mật.**

Hãy dùng tính năng báo cáo lỗ hổng riêng tư của GitHub:

➡ <https://github.com/eGovFramework/homebrew-egovframe/security/advisories/new>

Nếu kho lưu trữ chưa bật báo cáo lỗ hổng riêng tư, vui lòng báo cáo qua [cổng thông tin eGovFrame](https://www.egovframe.go.kr/) chính thức thay vì mở issue công khai.

Vui lòng nêu rõ:

- đối tượng bị ảnh hưởng (tên và phiên bản cask, workflow hoặc script)
- cách tái hiện và tác động bạn dự đoán
- những gì bạn đã làm để xác minh (hash, URL, log)

Báo cáo được xử lý riêng tư cho đến khi có bản sửa; ghi nhận người báo cáo nếu được yêu cầu.

## Phạm vi

Thuộc phạm vi:

- Các cask trong [`Casks/`](../../Casks): URL tải xuống, giá trị SHA-256 và script cài đặt. Cask cũ `egovframedev@4.2.1` chạy `postflight` tải biểu tượng bằng `curl` và xóa thuộc tính cách ly (quarantine) của macOS; hãy báo cáo mọi điều khiến việc này không an toàn.
- Tự động hóa: [`.github/workflows/`](../../.github/workflows) và [`scripts/`](../../scripts). Cask mới được tạo bằng cách tải các DMG chính thức và tính hash trong CI; cách khiến bước đó tạo ra hash sai, làm lộ token hoặc chạy đầu vào không tin cậy được coi là lỗ hổng.

Ngoài phạm vi, vui lòng báo cho bên chịu trách nhiệm:

- IDE eGovFrame và máy chủ tải xuống của nó → dự án eGovFrame, <https://www.egovframe.go.kr/> và [eGovFramework](https://github.com/eGovFramework).
- Bản thân Homebrew → <https://github.com/Homebrew/brew/security/policy>.
## Phiên bản được hỗ trợ

Chỉ những gì có trong `Casks/` trên nhánh mặc định (`main`) được duy trì: `egovframedev-latest` và các cask theo phiên bản nêu trong [README](../README.vi.md). Các cask đã bị xóa khi có bản vá mới hơn của cùng dòng thì không được duy trì.

## Tự xác minh bản tải xuống

Mỗi cask ghim một SHA-256 cho từng kiến trúc mà nó cung cấp, và mỗi [Release](https://github.com/eGovFramework/homebrew-egovframe/releases) đều liệt kê chúng. Một số cask theo phiên bản (ví dụ 3.10.0 và 4.0.0) chỉ dành cho Intel nên chỉ ghim một hash. Để kiểm tra lại một phiên bản với máy chủ chính thức từ CI:

```bash
gh workflow run update-casks.yml -R eGovFramework/homebrew-egovframe -f verify=5.0.2
```
