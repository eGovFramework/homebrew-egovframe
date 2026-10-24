# سياسة الأمان

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](SECURITY.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](SECURITY.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](SECURITY.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](SECURITY.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/flat.svg)](SECURITY.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](SECURITY.fr.md)

## الإبلاغ عن ثغرة

**يرجى عدم فتح issue عامة لمشكلة أمنية.**

استخدموا بدلًا من ذلك الإبلاغ الخاص عن الثغرات في GitHub:

➡ <https://github.com/eGovFramework/homebrew-egovframe/security/advisories/new>

إذا لم يكن الإبلاغ الخاص عن الثغرات مفعّلًا في المستودع، فيرجى الإبلاغ عبر [بوابة eGovFrame](https://www.egovframe.go.kr/) الرسمية بدلًا من فتح issue عامة.

يرجى تضمين ما يلي:

- ما الذي تأثر (اسم الـ cask وإصداره، أو سير العمل، أو السكربت)
- طريقة إعادة إنتاج المشكلة والأثر المتوقع
- أي شيء فعلتموه للتحقق منها (قيم التجزئة، الروابط، السجلات)

تُعالج البلاغات بسرّية حتى يتوفر إصلاح، ويُذكر اسم المُبلِّغ عند الطلب.

## النطاق

ضمن النطاق:

- ملفات cask في [`Casks/`](../../Casks): روابط التنزيل وقيم SHA-256 وسكربتات التثبيت. يشغّل الـ cask القديم `egovframedev@4.2.1` الخطوة `postflight` التي تنزّل أيقونة عبر `curl` وتزيل سمة الحجر (quarantine) في macOS؛ أبلغوا عن أي أمر يجعل ذلك غير آمن.
- الأتمتة: [`.github/workflows/`](../../.github/workflows) و[`scripts/`](../../scripts). تُنشأ ملفات cask الجديدة بتنزيل ملفات DMG الرسمية وحساب قيم تجزئتها في CI؛ وأي طريقة تجعل هذه الخطوة تنتج قيمة تجزئة خاطئة أو تسرّب الرمز (token) أو تشغّل مدخلات غير موثوقة تُعد ثغرة.

خارج النطاق، يرجى إبلاغ الجهة المسؤولة:

- بيئة eGovFrame IDE وخادم التنزيل الخاص بها ← مشروع eGovFrame، <https://www.egovframe.go.kr/> و[eGovFramework](https://github.com/eGovFramework).
- Homebrew نفسه ← <https://github.com/Homebrew/brew/security/policy>.
## الإصدارات المدعومة

يُصان فقط ما هو موجود في `Casks/` على الفرع الافتراضي (`main`): `egovframedev-latest` وملفات cask ذات الإصدارات المحددة المدرجة في [README](../README.ar.md). أما ملفات cask التي حُذفت عند صدور تصحيح أحدث من السلسلة نفسها فلا تُصان.

## التحقق من التنزيل بنفسك

يثبّت كل cask قيمة SHA-256 لكل معمارية يوفّرها، وتدرجها كل [إصدارة (Release)](https://github.com/eGovFramework/homebrew-egovframe/releases). بعض ملفات cask ذات الإصدارات المحددة (مثل 3.10.0 و4.0.0) مخصصة لـ Intel فقط، لذا تثبّت قيمة تجزئة واحدة. لإعادة فحص إصدار مقابل الخادم الرسمي من CI:

```bash
gh workflow run update-casks.yml -R eGovFramework/homebrew-egovframe -f verify=5.0.2
```
