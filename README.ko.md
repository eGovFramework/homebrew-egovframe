# homebrew-egovframe

## 소개
이곳은 eGovFrame의 Homebrew Tap(3rd party repository)입니다. 여기에는 eGovFrame의 통합 개발 환경(IDE)용 Cask들이 포함되어 있습니다.

## eGovFrame에 대하여
- 이름: egovframe
- 설명: eGovFrame은 대한민국 정부에서 제공하는 오픈 소스 프레임워크입니다. 이는 웹 기반 공공 서비스 개발을 위해 설계되었습니다. 정부 표준 개발 플랫폼으로서, eGovFrame은 공공 부문 IT 프로젝트에 중요한 역할을 합니다. 전 세계의 사용자가 사용할 수 있도록 공개되어 있습니다.
- 홈페이지: [eGovFrame 공식 웹사이트](https://www.egovframe.go.kr/)

## 사용 방법

eGovFrame IDE의 최신 버전을 설치하려면:

```bash
brew install egovframedev
```

특정 버전의 eGovFrame IDE를 설치하려면 다음 단계를 따르세요:

1. Homebrew에 eGovFramework 탭을 추가합니다:
   ```bash
   brew tap egovframework/egovframe
   ```
2. 원하는 버전의 eGovFrame IDE를 설치합니다:
   ```bash
   brew install egovframedev-latest
   brew install egovframedev@4.2.0
   brew install egovframedev@4.1.0
   brew install egovframedev@4.0.0
   brew install egovframedev@3.10.0
   ```

버전을 지정하는 것은 선택사항입니다. 생략하면 최신 버전이 설치됩니다.

## 앱 설치 경로
/Applications/ "응용 프로그램" 디렉토리 아래에 설치되며, "eGovFrameDev-X.X.0-Mac.app" 형식의 앱 이름으로 확인 가능합니다.
