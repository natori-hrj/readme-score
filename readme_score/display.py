"""スコア結果をリッチに表示するモジュール"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from readme_score.scorer import ScoreReport

console = Console()


def display_report(report: ScoreReport) -> None:
    """スコアレポートを表示する"""
    _display_header(report)
    _display_results_table(report)
    _display_suggestions(report)


def _display_header(report: ScoreReport) -> None:
    score = report.percentage
    if score >= 80:
        color = "green"
        grade = "A"
    elif score >= 60:
        color = "yellow"
        grade = "B"
    elif score >= 40:
        color = "red"
        grade = "C"
    else:
        color = "bright_red"
        grade = "D"

    score_text = Text(f" {score:.0f} / 100 ", style=f"bold {color}")
    grade_text = Text(f" Grade: {grade} ", style=f"bold {color}")

    title = f"README Score: {report.source}" if report.source else "README Score"
    panel = Panel(
        Text.assemble(score_text, "  ", grade_text),
        title=title,
        border_style=color,
    )
    console.print(panel)


def _display_results_table(report: ScoreReport) -> None:
    table = Table(show_header=True, header_style="bold")
    table.add_column("", width=3)
    table.add_column("チェック項目", min_width=30)
    table.add_column("配点", justify="right", width=6)
    table.add_column("得点", justify="right", width=6)

    for result in report.results:
        icon = "[green]✓[/green]" if result.passed else "[red]✗[/red]"
        points_style = "green" if result.passed else "red"
        table.add_row(
            icon,
            result.description,
            str(result.max_points),
            f"[{points_style}]{result.points}[/{points_style}]",
        )

    table.add_row("", "[bold]合計[/bold]", f"[bold]{report.max_score}[/bold]", f"[bold]{report.total_score}[/bold]")
    console.print(table)


def _display_suggestions(report: ScoreReport) -> None:
    suggestions = report.suggestions
    if not suggestions:
        console.print("\n[green bold]すべてのチェックをクリアしています！[/green bold]")
        return

    console.print(f"\n[yellow bold]改善提案 ({len(suggestions)}件):[/yellow bold]")
    for i, suggestion in enumerate(suggestions, 1):
        console.print(f"  {i}. {suggestion}")
