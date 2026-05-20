from datetime import datetime, timezone

import pytest


class TestYesterday:
    def test_returns_yesterday_date_formatted(self, mocker):
        mock_now = datetime(2026, 5, 20, 12, 0, tzinfo=timezone.utc)
        mocker.patch("game_fetcher.datetime").now.return_value = mock_now

        from game_fetcher import yesterday
        result = yesterday()

        assert result == "2026-05-19"

    def test_handles_month_wrap_around(self, mocker):
        mock_now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
        mocker.patch("game_fetcher.datetime").now.return_value = mock_now

        from game_fetcher import yesterday
        result = yesterday()

        assert result == "2025-12-31"