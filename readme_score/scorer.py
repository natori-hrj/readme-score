"""READMEの各項目をチェックしてスコアリングするモジュール"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from markdown_it import MarkdownIt


@dataclass
class CheckResult:
    name: str
    description: str
    passed: bool
    points: int
    max_points: int
    suggestion: str = ""


@dataclass
class ScoreReport:
    total_score: int = 0
    max_score: int = 0
    results: list[CheckResult] = field(default_factory=list)
    source: str = ""

    @property
    def percentage(self) -> float:
        if self.max_score == 0:
            return 0.0
        return (self.total_score / self.max_score) * 100

    @property
    def suggestions(self) -> list[str]:
        return [r.suggestion for r in self.results if not r.passed and r.suggestion]


CHECKS: list[dict] = [
    {
        "name": "title",
        "description": "タイトル（H1見出し）",
        "points": 15,
        "suggestion": "# で始まるタイトルを追加してください",
    },
    {
        "name": "description",
        "description": "プロジェクトの説明文",
        "points": 15,
        "suggestion": "タイトル直後にプロジェクトの概要を記述してください",
    },
    {
        "name": "installation",
        "description": "インストール手順",
        "points": 10,
        "suggestion": "## Installation セクションを追加してください",
    },
    {
        "name": "usage",
        "description": "使い方・サンプル",
        "points": 15,
        "suggestion": "## Usage セクションに使い方の例を追加してください",
    },
    {
        "name": "license",
        "description": "ライセンス情報",
        "points": 10,
        "suggestion": "## License セクションを追加してください",
    },
    {
        "name": "badges",
        "description": "バッジ（CI/CD、カバレッジ等）",
        "points": 5,
        "suggestion": "CI/CDやカバレッジのバッジを追加してください（例: GitHub Actions badge）",
    },
    {
        "name": "images",
        "description": "スクリーンショット・画像",
        "points": 5,
        "suggestion": "スクリーンショットやデモ画像を追加すると視覚的に伝わりやすくなります",
    },
    {
        "name": "contributing",
        "description": "コントリビューションガイド",
        "points": 10,
        "suggestion": "## Contributing セクションを追加してください",
    },
    {
        "name": "toc",
        "description": "目次（Table of Contents）",
        "points": 5,
        "suggestion": "## Table of Contents を追加すると長いREADMEが読みやすくなります",
    },
    {
        "name": "code_blocks",
        "description": "コードブロック",
        "points": 10,
        "suggestion": "コードブロック（```）でコマンドやコード例を示してください",
    },
]


def score_readme(content: str, source: str = "") -> ScoreReport:
    """README文字列を解析してスコアレポートを返す"""
    md = MarkdownIt()
    tokens = md.parse(content)
    report = ScoreReport(source=source)

    checkers = {
        "title": _check_title,
        "description": _check_description,
        "installation": _check_installation,
        "usage": _check_usage,
        "license": _check_license,
        "badges": _check_badges,
        "images": _check_images,
        "contributing": _check_contributing,
        "toc": _check_toc,
        "code_blocks": _check_code_blocks,
    }

    for check_def in CHECKS:
        name = check_def["name"]
        passed = checkers[name](content, tokens)
        points = check_def["points"] if passed else 0
        result = CheckResult(
            name=name,
            description=check_def["description"],
            passed=passed,
            points=points,
            max_points=check_def["points"],
            suggestion=check_def["suggestion"] if not passed else "",
        )
        report.results.append(result)
        report.total_score += points
        report.max_score += check_def["points"]

    return report


def _check_title(content: str, tokens: list) -> bool:
    """H1見出しがあるか"""
    for i, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag == "h1":
            if i + 1 < len(tokens) and tokens[i + 1].content.strip():
                return True
    return False


def _check_description(content: str, tokens: list) -> bool:
    """タイトル直後に説明文（段落）があるか"""
    found_h1 = False
    for token in tokens:
        if token.type == "heading_open" and token.tag == "h1":
            found_h1 = True
            continue
        if found_h1 and token.type == "heading_close" and token.tag == "h1":
            continue
        if found_h1 and token.type == "inline":
            continue
        if found_h1 and token.type == "paragraph_open":
            return True
        if found_h1 and token.type == "heading_open":
            return False
    return False


def _check_installation(content: str, tokens: list) -> bool:
    """インストール手順セクションがあるか"""
    return _has_section(tokens, r"install|setup|getting\s*started|導入|インストール")


def _check_usage(content: str, tokens: list) -> bool:
    """使い方セクションがあるか"""
    return _has_section(tokens, r"usage|how\s*to\s*use|example|使い方|使用方法")


def _check_license(content: str, tokens: list) -> bool:
    """ライセンス情報があるか"""
    return _has_section(tokens, r"license|ライセンス")


def _check_badges(content: str, tokens: list) -> bool:
    """バッジ画像（shields.io等）があるか"""
    badge_pattern = r"!\[.*?\]\(https?://.*?(shields\.io|badge|codecov|coveralls|github\.com/.*/(actions|workflows))"
    return bool(re.search(badge_pattern, content, re.IGNORECASE))


def _check_images(content: str, tokens: list) -> bool:
    """画像（スクリーンショット等）があるか"""
    image_pattern = r"!\[.*?\]\(.*?\.(png|jpg|jpeg|gif|svg|webp)"
    html_img_pattern = r"<img\s+.*?src="
    return bool(
        re.search(image_pattern, content, re.IGNORECASE)
        or re.search(html_img_pattern, content, re.IGNORECASE)
    )


def _check_contributing(content: str, tokens: list) -> bool:
    """コントリビューションガイドがあるか"""
    return _has_section(tokens, r"contribut|コントリビュー|貢献")


def _check_toc(content: str, tokens: list) -> bool:
    """目次があるか"""
    if _has_section(tokens, r"table\s*of\s*contents|目次|contents"):
        return True
    toc_link_pattern = r"\[.*?\]\(#.*?\)"
    links = re.findall(toc_link_pattern, content)
    return len(links) >= 3


def _check_code_blocks(content: str, tokens: list) -> bool:
    """コードブロックがあるか"""
    for token in tokens:
        if token.type == "fence" or token.type == "code_block":
            return True
    return False


def _has_section(tokens: list, pattern: str) -> bool:
    """指定パターンにマッチする見出しセクションがあるか"""
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                heading_text = tokens[i + 1].content
                if re.search(pattern, heading_text, re.IGNORECASE):
                    return True
    return False
