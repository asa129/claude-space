import json
from unittest.mock import patch

from main import main


FAKE_ARTICLES = [
    {"title": "Alpha", "url": "https://example.com/a", "score": 100},
    {"title": "Beta", "url": "https://example.com/b", "score": 50},
]


class TestMainOutput:
    @patch("main.fetch_news", return_value=FAKE_ARTICLES)
    def test_default_numbered_output(self, mock_fetch, capsys):
        with patch("sys.argv", ["main.py"]):
            main()

        out = capsys.readouterr().out
        assert "1." in out
        assert "Alpha" in out
        assert "2." in out
        assert "Beta" in out
        assert "Score: 100" in out

    @patch("main.fetch_news", return_value=FAKE_ARTICLES)
    def test_json_output(self, mock_fetch, capsys):
        with patch("sys.argv", ["main.py", "--json"]):
            main()

        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data) == 2
        assert data[0]["title"] == "Alpha"

    @patch("main.fetch_news", return_value=[])
    def test_limit_passed_to_fetch_news(self, mock_fetch):
        with patch("sys.argv", ["main.py", "--limit", "5"]):
            main()

        mock_fetch.assert_called_once_with(limit=5)
