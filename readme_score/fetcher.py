"""GitHubリポジトリURLからREADME.mdを取得するモジュール"""

from __future__ import annotations

import re
from pathlib import Path

import httpx


class FetchError(Exception):
    """README取得時のエラー"""


def read_local_file(path: str) -> str:
    """ローカルファイルを読み込む"""
    file_path = Path(path)
    if not file_path.exists():
        raise FetchError(f"ファイルが見つかりません: {path}")
    if not file_path.is_file():
        raise FetchError(f"ファイルではありません: {path}")
    return file_path.read_text(encoding="utf-8")


def fetch_from_github(url: str) -> str:
    """GitHubリポジトリURLからREADME.mdを取得する"""
    owner, repo = _parse_github_url(url)
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md"

    try:
        response = httpx.get(raw_url, follow_redirects=True, timeout=15.0)
    except httpx.HTTPError as e:
        raise FetchError(f"HTTP通信エラー: {e}") from e

    if response.status_code == 404:
        raise FetchError(f"README.mdが見つかりません: {url}")
    if response.status_code != 200:
        raise FetchError(
            f"取得に失敗しました (HTTP {response.status_code}): {url}"
        )

    return response.text


def _parse_github_url(url: str) -> tuple[str, str]:
    """GitHub URLからowner/repoを抽出する"""
    pattern = r"github\.com/([^/]+)/([^/\s?#]+)"
    match = re.search(pattern, url)
    if not match:
        raise FetchError(f"GitHubのURLとして認識できません: {url}")
    owner = match.group(1)
    repo = match.group(2).removesuffix(".git")
    return owner, repo
