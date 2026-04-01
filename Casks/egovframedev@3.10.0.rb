cask "egovframedev@3.10.0" do
  version "3.10.0"
  sha256 "c0b36911ba9e527d7f6f87481b183fcf2095756c0b84e36ce28c33c9094feb32"

  url "https://maven.egovframe.go.kr/publist/HDD1/public/eGovFrameDev-#{version}-Mac-64bit.dmg",
      user_agent: :fake
  name "egovframe"
  desc "Open-source framework by South Korea for web-based public service development"
  homepage "https://www.egovframe.go.kr/"

  app "eGovFrameDev-#{version}-Mac-64bit.app"

  zap trash: [
    "~/Library/Preferences/org.eclipse.platform.ide.plist",
    "~/Library/Saved Application State/org.eclipse.platform.ide.savedState",
  ]
end
