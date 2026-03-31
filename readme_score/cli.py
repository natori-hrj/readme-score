"""CLIエントリーポイント"""

from __future__ import annotations

import sys

import click

from readme_score.display import display_report
from readme_score.fetcher import FetchError, fetch_from_github, read_local_file
from readme_score.scorer import score_readme


@click.command()
@click.argument("file", required=False)
@click.option("--url", help="GitHubリポジトリのURL")
def main(file: str | None, url: str | None) -> None:
    """README.mdの品質をスコアリングするCLIツール"""
    if not file and not url:
        click.echo("エラー: ファイルパスまたは --url を指定してください", err=True)
        sys.exit(1)

    try:
        if url:
            content = fetch_from_github(url)
            source = url
        else:
            content = read_local_file(file)  # type: ignore[arg-type]
            source = file  # type: ignore[assignment]
    except FetchError as e:
        click.echo(f"エラー: {e}", err=True)
        sys.exit(1)

    report = score_readme(content, source=source)
    display_report(report)

    sys.exit(0 if report.percentage >= 50 else 1)
