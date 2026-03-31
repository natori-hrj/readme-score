# readme-score

README.md の品質を 100 点満点でスコアリングする CLI ツール。ローカルファイルと GitHub リポジトリ URL の両方に対応。

## Installation

```bash
pip install -e .
```

## Usage

```bash
# ローカルファイルを解析
readme-score ./README.md

# GitHub リポジトリを解析
readme-score --url https://github.com/user/repo
```

### 出力例

```
╭───────────── README Score: ./README.md ──────────────╮
│  80 / 100    Grade: A                                │
╰──────────────────────────────────────────────────────╯
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃     ┃ チェック項目                   ┃   配点 ┃   得点 ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ ✓   │ タイトル（H1見出し）           │     15 │     15 │
│ ✓   │ プロジェクトの説明文           │     15 │     15 │
│ ...                                                     │
└─────┴────────────────────────────────┴────────┴────────┘
```

## スコアリング項目

| チェック項目 | 配点 |
|---|---|
| タイトル（H1 見出し） | 15 |
| プロジェクトの説明文 | 15 |
| 使い方・サンプル | 15 |
| インストール手順 | 10 |
| ライセンス情報 | 10 |
| コントリビューションガイド | 10 |
| コードブロック | 10 |
| バッジ（CI/CD 等） | 5 |
| スクリーンショット・画像 | 5 |
| 目次 | 5 |

50 点未満の場合は終了コード 1 を返すため、CI での品質ゲートとしても利用可能。

## 技術スタック

- Python 3.10+
- [click](https://click.palletsprojects.com/) — CLI フレームワーク
- [markdown-it-py](https://github.com/executablebooks/markdown-it-py) — Markdown 解析
- [rich](https://github.com/Textualize/rich) — カラー表示
- [httpx](https://www.python-httpx.org/) — HTTP クライアント（GitHub URL 対応）

## Development

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## License

MIT
