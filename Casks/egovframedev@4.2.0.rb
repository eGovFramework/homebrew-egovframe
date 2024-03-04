cask "egovframedev@4.2.0" do
  arch arm: "AArch64", intel: "x86_64"

  version "4.2.0"
  sha256 arm:   "b6c5a3eae903cbc4bdffa490a97853330329a4215af8ae9d5cb8d45d3cbb34c6",
         intel: "40df38a8eb73df152b8425930e321f1e05b859143554adbbb03465dd904b4f0e"

  url "https://maven.egovframe.go.kr/publist/HDD1/public/eGovFrameDev-#{version}-Mac-#{arch}.dmg"
  name "egovframe"
  desc "Open-source framework by South Korea for web-based public service development"
  homepage "https://www.egovframe.go.kr/"

  app "eGovFrameDev-#{version}-Mac-#{arch}.app"

  postflight do
    icon_path = "#{Caskroom.path}/egovframedev@4.1.0/#{version}/app.icns"
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
