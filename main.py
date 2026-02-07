import argparse
import json

from scraper import fetch_news


def main():
    parser = argparse.ArgumentParser(description="Hacker Newsの技術ニュースを取得するCLIツール")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON形式で出力")
    parser.add_argument("--limit", type=int, default=10, help="表示件数（デフォルト: 10）")
    args = parser.parse_args()

    articles = fetch_news(limit=args.limit)

    if args.as_json:
        print(json.dumps(articles, ensure_ascii=False, indent=2))
    else:
        for i, article in enumerate(articles, 1):
            print(f"{i:>3}. {article['title']}")
            print(f"     スコア: {article['score']}  リンク: {article['url']}")
            print()


if __name__ == "__main__":
    main()
