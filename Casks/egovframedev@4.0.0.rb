cask "egovframedev@4.0.0" do

  version "4.0.0"
  sha256 "4ee5be1d0f67b35bfdf79194831a2b2b36a9836763821e80eebbccc94a711c06"

  url "https://maven.egovframe.go.kr/publist/HDD1/public/eGovFrameDev-#{version}-Mac-64bit.dmg", user_agent: :fake
  name "egovframe"
  desc "Open-source framework by South Korea for web-based public service development"
  homepage "https://www.egovframe.go.kr/"

  app "eGovFrameDev-#{version}-Mac-64bit.app"

  zap trash: [
    "~/Library/Preferences/org.eclipse.platform.ide.plist",
    "~/Library/Saved Application State/org.eclipse.platform.ide.savedState",
  ]
end

