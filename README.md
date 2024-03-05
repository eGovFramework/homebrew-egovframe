# homebrew-egovframe

## Introduction
Welcome to eGovFrame's Homebrew Tap, an external repository for Homebrew. This Tap is dedicated to hosting Casks for eGovFrame's Integrated Development Environment (IDE).

## About eGovFrame
- Name: eGovFrame
- Description: eGovFrame is an open-source framework provided by the government of South Korea. It is designed for the development of web-based public services. As a government-standardized development platform, eGovFrame plays a crucial role in IT projects within the public sector in Korea. Its global availability allows it to be utilized by users worldwide.
- Homepage: [eGovFrame Official Website](https://www.egovframe.go.kr/)

## Installation Guide

### For the Latest Version of eGovFrame IDE:

Simply run the following command in your terminal:
```bash
brew install egovframedev
```

### For Specific Versions of eGovFrame IDE:

1. Tap into the eGovFrame's repository:
   ```bash
   brew tap egovframework/egovframe
   ```
2. Install the desired version of eGovFrame IDE:
   ```bash
   brew install egovframedev-latest
   brew install egovframedev@4.2.0
   brew install egovframedev@4.1.0
   brew install egovframedev@4.0.0
   brew install egovframedev@3.10.0
   ```

Please note that specifying the version is optional. If omitted, the latest version will be installed.

### Application Installation Path

The application is installed under the `/Applications/` directory. The app will be named following the format "eGovFrameDev-X.X.0-Mac.app", where X.X.0 represents the version number.
