# دليل توقيع الشيفرة في macOS

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](code-signing-guideline.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](code-signing-guideline.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](code-signing-guideline.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](code-signing-guideline.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/flat.svg)](code-signing-guideline.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](code-signing-guideline.fr.md)

يتيح توقيع الشيفرة لنظام macOS التحقق من هوية من أنشأ التطبيق ومن أنه لم يتغير منذ توقيعه. تُوقَّع البرامج الموزعة خارج Mac App Store بشهادة **Developer ID Application** الصادرة عبر Apple Developer Program.

## التوقيع والتوثيق (notarization) خطوتان مختلفتان

- **التوقيع** (`codesign`) يُلحق توقيع Developer ID الخاص بك بالشيفرة، ويثبت مصدرها وسلامتها.
- **التوثيق** (`notarytool`) يرفع النسخة الموقّعة إلى Apple التي تفحصها آليًا وتصدر تذكرة (ticket). بموجب السياسة الافتراضية لـ Gatekeeper يُتوقع توثيق البرامج الموقّعة بـ Developer ID والموزعة خارج App Store؛ وينطبق ذلك منذ macOS 10.15 (Catalina) على البرامج المبنية بعد يونيو 2019.
- يتطلب التوثيق تفعيل Hardened Runtime (`--options runtime`) لأهداف التطبيقات وأدوات سطر الأوامر، وختمًا زمنيًا آمنًا (`--timestamp`) على كل توقيع.

## المتطلبات الأساسية

- سجّل في Apple Developer Program وأنشئ شهادة **Developer ID Application**. احتفظ بها مع مفتاحها الخاص في سلسلة مفاتيح جهاز Mac الذي يوقّع (مثل سلسلة مفاتيح تسجيل الدخول).
- ثبّت إصدارًا مدعومًا من Xcode يتضمن `notarytool` و`stapler`، ثم حدّد أدوات المطوّر الخاصة به (مثل `sudo xcode-select -s "/Applications/Xcode.app"`). الأداتان `codesign` و`spctl` مضمّنتان في macOS.
- وقّع فقط النسخ التي أنشأتها بنفسك أو التي تثق بها. التوقيع لا يجعل الشيفرة غير الموثوقة آمنة.
- لا يتطلب التوقيع تسجيل الدخول إلى iCloud.

## التوقيع من الداخل إلى الخارج

وقّع الشيفرة المتداخلة أولًا (dylib وframework وhelper وخدمات XPC والإضافات) ثم الحزمة الخارجية أخيرًا، بحيث يغطي كل توقيع محتوى موقّعًا مسبقًا. لا تعتمد على `--deep` للتوقيع: فهو يطبّق مجموعة الخيارات نفسها على كل شيء وApple لا توصي به للتوقيع. أضف `--entitlements "[FILE].entitlements"` فقط إذا احتاج التطبيق إلى entitlements.

```bash
# Developer ID Application identity (list available identities with: security find-identity -v -p codesigning)
IDENTITY="Developer ID Application: [NAME] ([TEAM_ID])"

# 1) الشيفرة المتداخلة أولًا
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[LIB].dylib"
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[NAME].framework"

# 2) حزمة التطبيق الخارجية أخيرًا
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app"
```

إذا فشل التوقيع بسبب بيانات وصفية زائدة (مثل resource forks أو ملفات Finder)، فأصلح مخرجات البناء أو انسخها نسخًا نظيفًا، مثل `ditto --norsrc --noextattr`. لا تحذف الخصائص الموسّعة من كل الملفات افتراضيًا.

## التحقق من التوقيع

تحقق باستخدام `codesign` ثم اسأل Gatekeeper باستخدام `spctl`. قبل التوثيق قد يرفض `spctl` التطبيق لأنه غير موثّق؛ وهذا متوقع.

```bash
codesign --verify --deep --strict --verbose=2 "[APP].app"
codesign --display --verbose=4 "[APP].app"
spctl --assess --type execute --verbose=4 "[APP].app"
```

## التوثيق والتدبيس (staple)

أرسل أرشيفًا (`.zip` أو `.dmg` أو `.pkg`) للتطبيق الموقّع، وليس ملف `.dylib` منفردًا. بعد القبول، ثبّت التذكرة (staple) وأعد التحقق أعلاه.

```bash
# One-time: store notarization credentials in the keychain (prompts for an app-specific password)
xcrun notarytool store-credentials "[PROFILE]" --apple-id "[APPLE_ID]" --team-id "[TEAM_ID]"

ditto -c -k --keepParent "[APP].app" "[APP].zip"
xcrun notarytool submit "[APP].zip" --keychain-profile "[PROFILE]" --wait
xcrun stapler staple "[APP].app"
xcrun stapler validate "[APP].app"
```

## المراجع

- <https://developer.apple.com/support/code-signing/>
- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- <https://developer.apple.com/documentation/security/customizing-the-notarization-workflow>
- <https://developer.apple.com/documentation/security/resolving-common-notarization-issues>
- <https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web>
- <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web>
