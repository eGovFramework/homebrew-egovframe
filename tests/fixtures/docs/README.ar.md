# homebrew-egovframe

<!-- latest-badge:start -->
[![الإطار القياسي للحكومة الإلكترونية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/unversioned/flat-ar.svg)](https://www.egovframe.go.kr/)
[![CI](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/ci.yml)
[![Update casks](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml/badge.svg)](https://github.com/leejongyoung/homebrew-egovframe/actions/workflows/update-casks.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](../LICENSE)
<!-- latest-badge:end -->

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](README.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](README.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](README.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](README.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/flat.svg)](README.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](README.fr.md)

## نبذة

حزم Homebrew Cask لبيئة التطوير المتكاملة (IDE) الخاصة بإطار عمل الحكومة الإلكترونية القياسي (eGovFrame) على نظام macOS. يتم تنزيل الحزم مباشرةً من الخادم الرسمي لـ eGovFrame.

- [الموقع الرسمي لـ eGovFrame](https://www.egovframe.go.kr/)
- [تنزيلات بيئة التطوير](https://www.egovframe.go.kr/home/sub.do?menuNo=40)
- [دليل توقيع الشيفرة](code-signing-guideline/code-signing-guideline.ar.md)

## التثبيت

### إضافة المستودع (Tap) الرسمي

قم بتثبيت [Homebrew](https://brew.sh/) أولاً، ثم أضف هذا المستودع مرة واحدة:

```bash
brew tap egovframework/egovframe
```

### تثبيت أحدث إصدار

```bash
brew install --cask egovframework/egovframe/egovframedev-latest
```

يحمل أحدث إصدار في هذا المستودع الاسم `egovframedev-latest`. استخدم هذا الاسم صراحةً عند التثبيت.

### تثبيت إصدار محدد

اختر أحد الإصدارات المتاحة:

```bash
brew install egovframedev@5.0.2
brew install egovframedev@4.3.1
brew install egovframedev@4.2.1
brew install egovframedev@4.1.1
brew install egovframedev@4.0.0
brew install egovframedev@3.10.0
```

إذا كان هناك مستودع آخر يحتوي على حزمة بنفس الاسم، فاستخدم الاسم الكامل `egovframework/egovframe/egovframedev@<version>`.

### تحديث أحدث إصدار

```bash
brew update
brew upgrade --cask egovframework/egovframe/egovframedev-latest
```

## المعماريات المدعومة ومسار التطبيق

- تدعم جميع الإصدارات المدرجة (باستثناء 3.10.0 و4.0.0) معماريتي Apple Silicon (ARM64) وIntel (x86_64)، ويختار Homebrew الحزمة المناسبة تلقائياً.
- يتوفر الإصداران 3.10.0 و4.0.0 لمعمارية Intel (x86_64) فقط.
- يتم تثبيت التطبيقات داخل المجلد `/Applications/`:
  - 3.10.0 و4.0.0: `eGovFrameDev-X.X.X-Mac-64bit.app`
  - الإصدارات ثنائية المعمارية بتسمية `Mac`: `eGovFrameDev-X.X.X-Mac-AArch64.app` أو `eGovFrameDev-X.X.X-Mac-x86_64.app`
  - الإصدارات ثنائية المعمارية بتسمية `macOS`: `eGovFrameDev-X.X.X-macOS-AArch64.app` أو `eGovFrameDev-X.X.X-macOS-x86_64.app`

## الترخيص

راجع [LICENSE](../LICENSE). تعود حقوق أسماء وشعارات eGovFrame إلى أصحابها المعنيين.
