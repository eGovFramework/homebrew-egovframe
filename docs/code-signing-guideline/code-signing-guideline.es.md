# Guía de firma de código en macOS

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](code-signing-guideline.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](code-signing-guideline.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/flat.svg)](code-signing-guideline.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](code-signing-guideline.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](code-signing-guideline.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](code-signing-guideline.fr.md)

La firma de código permite a macOS verificar quién creó una aplicación y que no se ha modificado desde que se firmó. El software distribuido fuera de la Mac App Store se firma con un certificado **Developer ID Application** emitido a través del Apple Developer Program.

## Firma y notarización son pasos distintos

- **Firmar** (`codesign`) adjunta su firma Developer ID al código. Demuestra el origen y la integridad del código.
- **Notarizar** (`notarytool`) sube la compilación firmada a Apple, que la analiza automáticamente y emite un ticket. Con la política predeterminada de Gatekeeper, se espera que el software firmado con Developer ID y distribuido fuera de la App Store esté notarizado; esto se aplica desde macOS 10.15 (Catalina) al software compilado después de junio de 2019.
- La notarización requiere habilitar el Hardened Runtime (`--options runtime`) en los destinos de app y de línea de comandos, y una marca de tiempo segura (`--timestamp`) en cada firma.

## Requisitos previos

- Inscríbase en el Apple Developer Program y cree un certificado **Developer ID Application**. Consérvelo, con su clave privada, en el llavero del Mac que firma (por ejemplo, el llavero de inicio de sesión).
- Instale una versión compatible de Xcode, que incluye `notarytool` y `stapler`, y seleccione sus herramientas de desarrollo (por ejemplo, `sudo xcode-select -s "/Applications/Xcode.app"`). `codesign` y `spctl` vienen con macOS.
- Firme solo compilaciones propias o de confianza. Firmar no hace seguro un código en el que no se confía.
- Firmar no requiere haber iniciado sesión en iCloud.

## Firmar de dentro hacia fuera

Firme primero el código anidado (dylibs, frameworks, helpers, servicios XPC, plug-ins) y por último el paquete exterior, de modo que cada firma cubra contenido ya firmado. No use `--deep` para firmar: aplica las mismas opciones a todo y Apple no lo recomienda para firmar. Añada `--entitlements "[FILE].entitlements"` solo si la app necesita entitlements.

```bash
# Developer ID Application identity (list available identities with: security find-identity -v -p codesigning)
IDENTITY="Developer ID Application: [NAME] ([TEAM_ID])"

# 1) Primero el código anidado
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[LIB].dylib"
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app/Contents/Frameworks/[NAME].framework"

# 2) Al final, el paquete de la app
codesign --force --timestamp --options runtime --sign "$IDENTITY" "[APP].app"
```

Si la firma falla por metadatos sobrantes (por ejemplo, resource forks o archivos del Finder), corrija la salida de compilación o cópiela limpiamente, por ejemplo con `ditto --norsrc --noextattr`. No elimine por defecto los atributos extendidos de todos los archivos.

## Verificar la firma

Verifique con `codesign` y consulte a Gatekeeper con `spctl`. Antes de la notarización, `spctl` puede rechazar la app por no estar notarizada; es lo esperado.

```bash
codesign --verify --deep --strict --verbose=2 "[APP].app"
codesign --display --verbose=4 "[APP].app"
spctl --assess --type execute --verbose=4 "[APP].app"
```

## Notarizar y grapar

Envíe un archivo (`.zip`, `.dmg` o `.pkg`) de la app firmada, no un `.dylib` suelto. Una vez aceptado, grape el ticket y repita la verificación anterior.

```bash
# One-time: store notarization credentials in the keychain (prompts for an app-specific password)
xcrun notarytool store-credentials "[PROFILE]" --apple-id "[APPLE_ID]" --team-id "[TEAM_ID]"

ditto -c -k --keepParent "[APP].app" "[APP].zip"
xcrun notarytool submit "[APP].zip" --keychain-profile "[PROFILE]" --wait
xcrun stapler staple "[APP].app"
xcrun stapler validate "[APP].app"
```

## Referencias

- <https://developer.apple.com/support/code-signing/>
- <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- <https://developer.apple.com/documentation/security/customizing-the-notarization-workflow>
- <https://developer.apple.com/documentation/security/resolving-common-notarization-issues>
- <https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web>
- <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web>
