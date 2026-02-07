import requests
from bs4 import BeautifulSoup


def fetch_news(limit=10):
    """Hacker Newsのトップページから記事情報を取得する。

    Args:
        limit: 取得する記事数

    Returns:
        記事情報の辞書リスト（title, url, score）
    """
    url = "https://news.ycombinator.com/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    rows = soup.select("tr.athing")

    for row in rows[:limit]:
        title_el = row.select_one(".titleline > a")
        if not title_el:
            continue

        title = title_el.get_text()
        link = title_el.get("href", "")

        # HN内部リンクの場合はフルURLに変換
        if link.startswith("item?"):
            link = f"https://news.ycombinator.com/{link}"

        # スコアは次の兄弟行にある
        score_row = row.find_next_sibling("tr")
        score = 0
        if score_row:
            score_el = score_row.select_one(".score")
            if score_el:
                score_text = score_el.get_text()  # e.g. "123 points"
                score = int(score_text.split()[0])

        articles.append({"title": title, "url": link, "score": score})

    return articles
