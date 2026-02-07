**このプロジェクトは Claude Code を使用して作成されました。**

# Hacker News CLIツール

Hacker News のトップページから技術ニュースを取得して表示するコマンドラインツールです。

## セットアップ

```bash
pip3 install -r requirements.txt
```

## 使い方

```bash
# トップ10件を表示
python3 main.py

# 表示件数を指定
python3 main.py --limit 5

# JSON形式で出力
python3 main.py --json

# 組み合わせ
python3 main.py --json --limit 3
```

### 出力例

```
  1. 記事タイトル
     スコア: 150  リンク: https://example.com/article

  2. 別の記事タイトル
     スコア: 42  リンク: https://example.com/another
```

## テスト

```bash
python3 -m pytest test_scraper.py test_main.py -v
```
