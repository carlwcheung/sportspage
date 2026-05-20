import unittest
from datetime import datetime, timezone
from unittest.mock import patch


class TestYesterday(unittest.TestCase):
    @patch("game_fetcher.datetime")
    def test_returns_yesterday_date_formatted(self, mock_datetime):
        mock_now = datetime(2026, 5, 20, 12, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now

        from game_fetcher import yesterday
        result = yesterday()

        self.assertEqual(result, "2026-05-19")

    @patch("game_fetcher.datetime")
    def test_handles_month_wrap_around(self, mock_datetime):
        mock_now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now

        from game_fetcher import yesterday
        result = yesterday()

        self.assertEqual(result, "2025-12-31")


if __name__ == "__main__":
    unittest.main()