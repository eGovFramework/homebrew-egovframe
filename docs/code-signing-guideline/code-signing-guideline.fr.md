# Guide de signature de code sur macOS

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](code-signing-guideline.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](code-signing-guideline.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](code-signing-guideline.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](code-signing-guideline.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](code-signing-guideline.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/flat.svg)](code-signing-guideline.fr.md)

La signature de code permet à macOS de vérifier qui a créé une application et qu'elle n'a pas été modifiée depuis sa signature. Les logiciels distribués en dehors du Mac App Store sont signés avec un certificat **Developer ID Application** émis via l'Apple Developer Program.

## Signature et notarisation sont deux étapes distinctes

- **Signer** (`codesign`) associe votre signature Developer ID au code. Elle prouve l'origine et l'intégrité du code.
- **Notariser** (`notarytool`) envoie la build signée à Apple, qui l'analyse automatiquement et délivre un ticket. Selon la politique par défaut de Gatekeeper, les logiciels signés Developer ID et distribués hors App Store doivent être notarisés ; cela s'applique depuis macOS 10.15 (Catalina) aux logiciels compilés après juin 2019.
- La notarisation exige d'activer le Hardened Runtime (`--options runtime`) pour les cibles d'app et de ligne de commande, ainsi qu'un horodatage sécurisé (`--timestamp`) sur chaque signature.

## Prérequis

- Inscrivez-vous à l'Apple Developer Program et créez un certificat **Developer ID Application**. Conservez-le, avec sa clé privée, dans le trousseau du Mac qui signe (par exemple le trousseau de session).
- Installez une version prise en charge de Xcode, qui inclut `notarytool` et `stapler`, et sélectionnez ses outils de développement (par exemple `sudo xcode-select -s "/Applications/Xcode.app"`). `codesign` et `spctl` sont fournis avec macOS.
- Ne signez que des builds que vous avez produites ou en lesquelles vous avez confiance. Signer ne rend pas sûr un code non fiable.
- La signature ne nécessite pas d'être connecté à iCloud.

## Signer de l'intérieur vers l'extérieur

Signez d'abord le code imbriqué (dylibs, frameworks, helpers, services XPC, plug-ins), puis le bundle externe en dernier, afin que chaque signature couvre un contenu déjà signé. Ne comptez pas sur `--deep` pour signer : il applique les mêmes options à tout et Apple le déconseille pour la signature. N'ajoutez `--entitlements "[FILE].entitlements"` que si l'app nécessite des entitlements.

```bash
# Developer ID Application identity (list available identities with: security find-identity -v -p codesigning)
IDENTITY="Developer ID Application: [NAME] ([TEAM_ID])"

# 1) D'abord le code imbriqué
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[LIB].dylib"
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[NAME].framework"

# 2) Enfin, le bundle de l'app
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app"
```

Si la signature échoue à cause de métadonnées parasites (par exemple des resource forks ou des fichiers du Finder), corrigez la sortie de build ou copiez-la proprement, par exemple avec `ditto --norsrc --noextattr`. Ne supprimez pas par défaut les attributs étendus de tous les fichiers.

## Vérifier la signature

Vérifiez avec `codesign`, puis interrogez Gatekeeper avec `spctl`. Avant la notarisation, `spctl` peut rejeter l'app comme non notarisée ; c'est normal.

```bash
codesign --verify --deep --strict --verbose=2 "[APP].app"
codesign --display --verbose=4 "[APP].app"
spctl --assess --type execute --verbose=4 "[APP].app"
```

## Notariser et agrafer

Soumettez une archive (`.zip`, `.dmg` ou `.pkg`) de l'app signée, pas un `.dylib` isolé. Une fois acceptée, agrafez le ticket (staple) et relancez la vérification ci-dessus.

```bash
# One-time: store notarization credentials in the keychain (prompts for an app-specific password)
xcrun notarytool store-credentials "[PROFILE]" --apple-id "[APPLE_ID]" --team-id "[TEAM_ID]"

ditto -c -k --keepParent "[APP].app" "[APP].zip"
xcrun notarytool submit "[APP].zip" --keychain-profile "[PROFILE]" --wait
xcrun stapler staple "[APP].app"
xcrun stapler validate "[APP].app"
```

## Références

- <https://developer.apple.com/support/code-signing/>
- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- <https://developer.apple.com/documentation/security/customizing-the-notarization-workflow>
- <https://developer.apple.com/documentation/security/resolving-common-notarization-issues>
- <https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web>
- <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web>
