from datetime import datetime, timedelta, timezone

from nba_client import NBAClient
from config import FOLLOWED_TEAMS, FORCE_PLAYOFF_MODE


def yesterday() -> str:
    d = datetime.now(timezone.utc) - timedelta(days=1)
    return d.strftime("%Y-%m-%d")


def _is_playoff_season(client: NBAClient) -> bool:
    if FORCE_PLAYOFF_MODE is not None:
        return FORCE_PLAYOFF_MODE
    today = datetime.now(timezone.utc)
    month = today.month
    return month in (4, 5, 6)


def _team_is_followed(game: dict) -> bool:
    if not FOLLOWED_TEAMS:
        return True
    home_name = game.get("teams", {}).get("home", {}).get("name", "")
    vis_name = game.get("teams", {}).get("visitors", {}).get("name", "")
    home_id = game.get("teams", {}).get("home", {}).get("id")
    vis_id = game.get("teams", {}).get("visitors", {}).get("id")
    for team in FOLLOWED_TEAMS:
        if team.lower() in (home_name.lower(), vis_name.lower()):
            return True
        try:
            tid = int(team)
            if tid in (home_id, vis_id):
                return True
        except ValueError:
            pass
    return False


def fetch_games(client: NBAClient, date_str: str | None = None) -> list[dict]:
    if date_str is None:
        date_str = yesterday()
    games = client.get_games(date_str)
    if not games:
        return []
    is_playoffs = _is_playoff_season(client)
    finished = [g for g in games if g.get("status", {}).get("short") == 3]
    if is_playoffs:
        return finished
    return [g for g in finished if _team_is_followed(g)]
