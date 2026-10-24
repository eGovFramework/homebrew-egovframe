# Política de seguridad

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](SECURITY.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](SECURITY.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/flat.svg)](SECURITY.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/outline.svg)](SECURITY.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](SECURITY.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](SECURITY.fr.md)

## Cómo informar de una vulnerabilidad

**No abra una incidencia pública para un problema de seguridad.**

Use en su lugar el informe privado de vulnerabilidades de GitHub:

➡ <https://github.com/eGovFramework/homebrew-egovframe/security/advisories/new>

Si el informe privado de vulnerabilidades no está habilitado en el repositorio, informe a través del [portal oficial de eGovFrame](https://www.egovframe.go.kr/) en lugar de abrir una incidencia pública.

Incluya, por favor:

- qué se ve afectado (nombre y versión del cask, flujo de trabajo o script)
- cómo reproducirlo y el impacto que espera
- lo que ya haya hecho para verificarlo (hashes, URL, registros)

Los informes se tratan de forma privada hasta que haya una corrección; se da crédito a quien lo solicite.

## Alcance

Dentro del alcance:

- Casks en [`Casks/`](../../Casks): URL de descarga, valores SHA-256 y scripts de instalación. El cask heredado `egovframedev@4.2.1` ejecuta un `postflight` que descarga un icono con `curl` y elimina el atributo de cuarentena de macOS; informe de cualquier cosa que lo haga inseguro.
- Automatización: [`.github/workflows/`](../../.github/workflows) y [`scripts/`](../../scripts). Los casks nuevos se generan descargando los DMG oficiales y calculando su hash en CI; una forma de hacer que ese paso produzca un hash incorrecto, filtre el token o ejecute entradas no confiables cuenta como vulnerabilidad.

Fuera del alcance, infórmelo al responsable:

- El IDE de eGovFrame y su servidor de descargas → el proyecto eGovFrame, <https://www.egovframe.go.kr/> y [eGovFramework](https://github.com/eGovFramework).
- Homebrew en sí → <https://github.com/Homebrew/brew/security/policy>.
## Versiones compatibles

Solo se mantiene lo que está en `Casks/` de la rama predeterminada (`main`): `egovframedev-latest` y los casks con versión indicados en el [README](../README.es.md). Los casks eliminados al llegar un parche más reciente de la misma serie no se mantienen.

## Verificar una descarga por su cuenta

Cada cask fija un SHA-256 para cada arquitectura que ofrece, y cada [Release](https://github.com/eGovFramework/homebrew-egovframe/releases) los enumera. Algunos casks con versión (por ejemplo 3.10.0 y 4.0.0) son solo para Intel, por lo que fijan un único hash. Para volver a comprobar una versión con el servidor oficial desde CI:

```bash
gh workflow run update-casks.yml -R eGovFramework/homebrew-egovframe -f verify=5.0.2
```
