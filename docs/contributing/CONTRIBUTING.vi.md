# Hướng dẫn đóng góp

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/flat.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](CONTRIBUTING.fr.md)

## Trước khi mở pull request

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # kiểm thử các script
brew style egovframework/egovframe/egovframedev-latest   # cần có tap: brew tap egovframework/egovframe
```

CI (`ci.yml`) chạy các kiểm thử cùng với `scripts/check_tap.sh` (`brew readall`, `brew style` và `brew audit`). Hãy chạy các lệnh từ thư mục gốc của kho; kiểm thử script cần PyYAML, và CI cài đặt theo cùng cách.

- Thông điệp commit theo phong cách đã dùng ở kho chính thức: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- Không sửa tay SHA-256 của cask. Phiên bản mới được tạo bởi `scripts/update_casks.py` (quy trình `Update casks`); để kiểm tra lại một hash hiện có, chạy `gh workflow run update-casks.yml -f verify=<version>`.
- Mỗi dòng phiên bản phụ chỉ giữ một cask: khi thêm `5.0.3` thì xóa `5.0.2` (cùng quy ước với kho chính thức).

## GitHub Actions và chi phí

- **Miễn phí trên kho công khai:** theo chính sách thanh toán của GitHub, các runner tiêu chuẩn do GitHub lưu trữ (`ubuntu-latest`, `macos-latest`) **miễn phí và không giới hạn số phút trên kho công khai**. Các tệp DMG được tính hash theo luồng trong `update-casks.yml` và không bao giờ được tải lên dưới dạng artifact của Actions hay tài sản của Release, nên cũng không tốn dung lượng lưu trữ của Actions.
- Số phút chỉ bị trừ vào hạn mức miễn phí của tài khoản nếu bạn sao chép kho sang kho riêng tư và chạy ở đó.

## Bảo mật

Không báo cáo lỗ hổng bảo mật qua issue; hãy làm theo quy trình trong [SECURITY.vi.md](../security/SECURITY.vi.md).
