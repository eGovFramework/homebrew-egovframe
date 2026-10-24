cask "egovframedev@4.2.1" do
  arch arm: "AArch64", intel: "x86_64"

  version "4.2.1"
  sha256 arm:   "10e6343cdc1e4c1d74dbffe5cecc4eca8ef7a589a699f96c5bad30d54ec452ef",
         intel: "03b63c59d1f458f7ffb0bc16e3efa03fd146fecd862228c8cbdb6e0bad623847"

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

  postflight do
    icon_path = "#{Caskroom.path}/egovframedev@4.2.1/#{version}/app.icns"
    app_path = "/Applications/eGovFrameDev-#{version}-Mac-#{arch}.app"
    system_command "mkdir", args: ["-p", File.dirname(icon_path)]
    system_command "curl", args: ["-s", "-o", icon_path, "https://maven.egovframe.go.kr/publist/HDD1/public/app.icns"]
    system_command "xattr", args: ["-d", "com.apple.quarantine", app_path]
    system_command "cp", args: [icon_path, "#{app_path}/Contents/Resources/Eclipse.icns"]
    system_command "touch", args: [app_path]
  end

  zap trash: [
    "~/Library/Preferences/org.eclipse.platform.ide.plist",
    "~/Library/Saved Application State/org.eclipse.platform.ide.savedState",
  ]
end
