"""scorerモジュールのテスト"""

from readme_score.scorer import score_readme


FULL_README = """\
# My Project

A great project that does amazing things.

[![CI](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/user/repo/actions)

![screenshot](./screenshot.png)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install my-project
```

## Usage

```python
from my_project import hello
hello()
```

## Contributing

PRs welcome!

## License

MIT
"""

MINIMAL_README = """\
# Hello
"""

EMPTY_README = ""


class TestScoreReadme:
    def test_full_readme_high_score(self):
        report = score_readme(FULL_README)
        assert report.percentage == 100.0
        assert report.total_score == report.max_score

    def test_minimal_readme_low_score(self):
        report = score_readme(MINIMAL_README)
        assert report.percentage < 50
        assert report.total_score == 15  # タイトルのみ

    def test_empty_readme(self):
        report = score_readme(EMPTY_README)
        assert report.total_score == 0

    def test_suggestions_for_minimal(self):
        report = score_readme(MINIMAL_README)
        assert len(report.suggestions) > 0

    def test_no_suggestions_for_full(self):
        report = score_readme(FULL_README)
        assert len(report.suggestions) == 0

    def test_source_stored(self):
        report = score_readme(MINIMAL_README, source="test.md")
        assert report.source == "test.md"

    def test_max_score_is_100(self):
        report = score_readme(EMPTY_README)
        assert report.max_score == 100


class TestIndividualChecks:
    def test_title_check(self):
        report = score_readme("# Title\n")
        title_result = next(r for r in report.results if r.name == "title")
        assert title_result.passed

    def test_no_title(self):
        report = score_readme("Just some text\n")
        title_result = next(r for r in report.results if r.name == "title")
        assert not title_result.passed

    def test_description_after_title(self):
        report = score_readme("# Title\n\nThis is a description.\n")
        desc_result = next(r for r in report.results if r.name == "description")
        assert desc_result.passed

    def test_no_description(self):
        report = score_readme("# Title\n\n## Section\n")
        desc_result = next(r for r in report.results if r.name == "description")
        assert not desc_result.passed

    def test_code_blocks(self):
        report = score_readme("# T\n\n```python\nprint('hi')\n```\n")
        cb_result = next(r for r in report.results if r.name == "code_blocks")
        assert cb_result.passed

    def test_badges_shields_io(self):
        content = "# T\n\n![badge](https://img.shields.io/badge/test-pass-green)\n"
        report = score_readme(content)
        badge_result = next(r for r in report.results if r.name == "badges")
        assert badge_result.passed

    def test_images_with_html_img(self):
        content = '# T\n\n<img src="demo.png" alt="demo">\n'
        report = score_readme(content)
        img_result = next(r for r in report.results if r.name == "images")
        assert img_result.passed

    def test_toc_with_anchor_links(self):
        content = "# T\n\n[A](#a)\n[B](#b)\n[C](#c)\n[D](#d)\n"
        report = score_readme(content)
        toc_result = next(r for r in report.results if r.name == "toc")
        assert toc_result.passed

    def test_japanese_section_names(self):
        content = "# プロジェクト\n\n説明文です。\n\n## インストール\n\n手順\n\n## 使い方\n\n例\n\n## ライセンス\n\nMIT\n\n## コントリビューション\n\nPR歓迎\n"
        report = score_readme(content)
        install = next(r for r in report.results if r.name == "installation")
        usage = next(r for r in report.results if r.name == "usage")
        license_r = next(r for r in report.results if r.name == "license")
        contrib = next(r for r in report.results if r.name == "contributing")
        assert install.passed
        assert usage.passed
        assert license_r.passed
        assert contrib.passed
