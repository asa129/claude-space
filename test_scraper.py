from unittest.mock import patch, Mock

import pytest
import requests

from scraper import fetch_news


def _make_html(articles):
    """Hacker News風のHTMLを生成するヘルパー。

    articles: list of dict with keys: title, url, score (optional)
    """
    rows = []
    for i, a in enumerate(articles):
        title = a["title"]
        url = a["url"]
        score = a.get("score")
        rows.append(
            f'<tr class="athing" id="{100 + i}">'
            f'<td class="title"><span class="titleline"><a href="{url}">{title}</a></span></td>'
            f"</tr>"
        )
        score_html = ""
        if score is not None:
            score_html = f'<span class="score">{score} points</span>'
        rows.append(f"<tr>{score_html}</tr>")
    return f"<html><body><table>{''.join(rows)}</table></body></html>"


def _mock_response(html, status_code=200):
    resp = Mock()
    resp.text = html
    resp.status_code = status_code
    resp.raise_for_status = Mock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=resp
        )
    return resp


class TestFetchNewsNormal:
    """正常系テスト"""

    @patch("scraper.requests.get")
    def test_extracts_title_url_score(self, mock_get):
        html = _make_html([
            {"title": "Article A", "url": "https://example.com/a", "score": 150},
            {"title": "Article B", "url": "https://example.com/b", "score": 42},
        ])
        mock_get.return_value = _mock_response(html)

        result = fetch_news(limit=10)

        assert len(result) == 2
        assert result[0] == {"title": "Article A", "url": "https://example.com/a", "score": 150}
        assert result[1] == {"title": "Article B", "url": "https://example.com/b", "score": 42}

    @patch("scraper.requests.get")
    def test_limit_controls_count(self, mock_get):
        html = _make_html([
            {"title": f"Art {i}", "url": f"https://example.com/{i}", "score": i}
            for i in range(5)
        ])
        mock_get.return_value = _mock_response(html)

        result = fetch_news(limit=2)

        assert len(result) == 2

    @patch("scraper.requests.get")
    def test_internal_link_converted_to_full_url(self, mock_get):
        html = _make_html([
            {"title": "Show HN", "url": "item?id=12345", "score": 10},
        ])
        mock_get.return_value = _mock_response(html)

        result = fetch_news()

        assert result[0]["url"] == "https://news.ycombinator.com/item?id=12345"

    @patch("scraper.requests.get")
    def test_missing_score_defaults_to_zero(self, mock_get):
        html = _make_html([
            {"title": "No Score", "url": "https://example.com/x"},
        ])
        mock_get.return_value = _mock_response(html)

        result = fetch_news()

        assert result[0]["score"] == 0

    @patch("scraper.requests.get")
    def test_row_without_titleline_is_skipped(self, mock_get):
        # 手動でtitlelineなしの行を作る
        html = (
            "<html><body><table>"
            '<tr class="athing" id="1"><td>no titleline here</td></tr>'
            "<tr></tr>"
            '<tr class="athing" id="2">'
            '<td class="title"><span class="titleline"><a href="https://example.com">Real</a></span></td>'
            "</tr>"
            '<tr><span class="score">5 points</span></tr>'
            "</table></body></html>"
        )
        mock_get.return_value = _mock_response(html)

        result = fetch_news()

        assert len(result) == 1
        assert result[0]["title"] == "Real"


class TestFetchNewsErrors:
    """エラー系テスト"""

    @patch("scraper.requests.get")
    def test_http_error_raises(self, mock_get):
        mock_get.return_value = _mock_response("", status_code=500)

        with pytest.raises(requests.exceptions.HTTPError):
            fetch_news()

    @patch("scraper.requests.get")
    def test_connection_error_raises(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("refused")

        with pytest.raises(requests.exceptions.ConnectionError):
            fetch_news()
