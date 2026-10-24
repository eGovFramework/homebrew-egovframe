cask "egovframedev@4.1.1" do
  arch arm: "AArch64", intel: "x86_64"

  version "4.1.1"
  sha256 arm:   "98610884ef5d10fb2617d443e2ad830179f133fdecc02bcf96bacb00b96fa565",
         intel: "68f94b26802c074f970147edb87938bc667efc83d1202e12b808ebc47a6090c4"

  url "https://maven.egovframe.go.kr/publist/HDD1/public/egovframework_v#{version.major_minor}/2_DevelopmentEnvironment/eGovFrame-Dev/#{version}/eGovFrameDev-#{version}-Mac-#{arch}.dmg",
      user_agent: :fake
  name "egovframe"
  desc "Open-source framework by South Korea for web-based public service development"
  homepage "https://www.egovframe.go.kr/"

  livecheck do
    url "https://www.egovframe.go.kr/home/sub.do?menuNo=40"
    regex(/개발자용\s개발환경\s(\d+(?:\.\d+)+).*/i)
  end

  depends_on :macos

  app "eGovFrameDev-#{version}-Mac-#{arch}.app"

  zap trash: [
    "~/Library/Preferences/org.eclipse.platform.ide.plist",
    "~/Library/Saved Application State/org.eclipse.platform.ide.savedState",
  ]
end
