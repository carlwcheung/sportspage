import requests

from config import API_SPORTS_KEY, NBA_API_BASE


class NBAClient:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({"x-apisports-key": API_SPORTS_KEY})
        self._teams_cache: list[dict] | None = None

    def _get(self, endpoint: str, params: dict | None = None) -> dict | None:
        url = f"{NBA_API_BASE}/{endpoint}"
        try:
            resp = self._session.get(url, params=params, timeout=15)
        except requests.RequestException:
            return None
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("errors"):
            return None
        return data

    def get_games(self, date: str) -> list[dict]:
        data = self._get("games", {"date": date})
        if not data:
            return []
        return data.get("response", [])

    def get_standings(self, season: int, league: str = "standard") -> list[dict]:
        data = self._get("standings", {"season": season, "league": league})
        if not data:
            return []
        return data.get("response", [])

    def get_teams(self) -> list[dict]:
        if self._teams_cache is not None:
            return self._teams_cache
        data = self._get("teams")
        if not data:
            return []
        self._teams_cache = data.get("response", [])
        return self._teams_cache
