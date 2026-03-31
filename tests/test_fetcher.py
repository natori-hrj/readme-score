"""fetcherモジュールのテスト"""

import pytest

from readme_score.fetcher import FetchError, _parse_github_url, read_local_file


class TestParseGithubUrl:
    def test_standard_url(self):
        assert _parse_github_url("https://github.com/user/repo") == ("user", "repo")

    def test_url_with_git_suffix(self):
        assert _parse_github_url("https://github.com/user/repo.git") == ("user", "repo")

    def test_url_with_path(self):
        assert _parse_github_url("https://github.com/user/repo/tree/main") == ("user", "repo")

    def test_invalid_url(self):
        with pytest.raises(FetchError, match="GitHubのURLとして認識できません"):
            _parse_github_url("https://example.com/foo")


class TestReadLocalFile:
    def test_missing_file(self):
        with pytest.raises(FetchError, match="ファイルが見つかりません"):
            read_local_file("/nonexistent/file.md")

    def test_read_existing_file(self, tmp_path):
        f = tmp_path / "README.md"
        f.write_text("# Test\n", encoding="utf-8")
        assert read_local_file(str(f)) == "# Test\n"
