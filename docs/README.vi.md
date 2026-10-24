# homebrew-egovframe

<!-- latest-badge:start -->
[![Khung chuẩn Chính phủ điện tử](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/unversioned/flat-vi.svg)](https://www.egovframe.go.kr/)
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../LICENSE)
<!-- latest-badge:end -->

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](README.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](README.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](README.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/flat.svg)](README.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](README.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](README.fr.md)

## Giới thiệu

Homebrew tap cung cấp các cask cho môi trường phát triển tích hợp (IDE) eGovFrame trên macOS. Các gói cài đặt được tải trực tiếp từ máy chủ chính thức của eGovFrame.

- [Trang chủ chính thức của eGovFrame](https://www.egovframe.go.kr/)
- [Tải xuống môi trường phát triển](https://www.egovframe.go.kr/home/sub.do?menuNo=40)
- [Hướng dẫn ký mã (code signing)](code-signing-guideline/code-signing-guideline.vi.md)

## Cài đặt

### Thêm tap chính thức

Cài đặt [Homebrew](https://brew.sh/) trước, sau đó thêm tap này một lần:

```bash
brew tap egovframework/egovframe
```

### Cài đặt phiên bản mới nhất

```bash
brew install --cask egovframework/egovframe/egovframedev-latest
```

Cask cho phiên bản mới nhất trong tap này có tên là `egovframedev-latest`. Hãy chỉ định rõ tên này khi cài đặt.

### Cài đặt phiên bản cụ thể

Chọn một trong các phiên bản hiện có:

```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

Nếu một tap khác có cask trùng tên, hãy chỉ định tên đầy đủ theo dạng `egovframework/egovframe/egovframedev@<version>`.

### Cập nhật cask mới nhất

```bash
brew update
brew upgrade --cask egovframework/egovframe/egovframedev-latest
```

## Kiến trúc hỗ trợ và đường dẫn ứng dụng

- Tất cả các cask ngoại trừ 3.10.0 và 4.0.0 đều hỗ trợ cả Apple Silicon (ARM64) và Intel (x86_64); Homebrew sẽ tự động chọn gói phù hợp.
- Phiên bản 3.10.0 và 4.0.0 chỉ cung cấp bản dựng cho Intel (x86_64).
- Ứng dụng được cài đặt tại `/Applications/`:
  - 3.10.0 và 4.0.0: `eGovFrameDev-X.X.X-Mac-64bit.app`
  - Cask đa kiến trúc dùng tên `Mac`: `eGovFrameDev-X.X.X-Mac-AArch64.app` hoặc `eGovFrameDev-X.X.X-Mac-x86_64.app`
  - Cask đa kiến trúc dùng tên `macOS`: `eGovFrameDev-X.X.X-macOS-AArch64.app` hoặc `eGovFrameDev-X.X.X-macOS-x86_64.app`

## Giấy phép

Xem [LICENSE](../LICENSE). Tên gọi và biểu trưng eGovFrame thuộc quyền sở hữu của các chủ sở hữu tương ứng.
