class EgovframeScaffoldMcp < Formula
  desc "eGovFrame project scaffolding MCP server for AI tools (Claude, Copilot, Cursor)"
  homepage "https://github.com/EricSeokgon/egovframe-scaffold-mcp"
  url "https://registry.npmjs.org/egovframe-scaffold-mcp/-/egovframe-scaffold-mcp-0.19.0.tgz"
  sha256 "0f320707db159177d7e40d5b3ee3f78b62a2cf9b5071e2d75fa9e0683f4e45bb"
  license "Apache-2.0"

  depends_on "node"

  def install
    system "npm", "install", *std_npm_args
    bin.install_symlink Dir["#{libexec}/bin/*"]
  end

  test do
    # MCP 서버는 stdio 기반이라 --help 대신 실행 파일 설치 여부를 검증한다
    assert_predicate bin/"egovframe-scaffold-mcp", :exist?
    assert_predicate bin/"egovframe-scaffold-mcp", :executable?
  end
end
