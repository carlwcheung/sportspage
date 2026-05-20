from nba_client import NBAClient
from game_fetcher import fetch_games
from email_sender import ConsoleSender


def _format_summary(games: list[dict], date_str: str) -> str:
    lines = [f"NBA Results — {date_str}"]
    if not games:
        lines.append("")
        lines.append("No games found.")
        return "\n".join(lines)
    for g in games:
        teams = g.get("teams", {})
        scores = g.get("scores", {})
        home_name = teams.get("home", {}).get("name", "?")
        vis_name = teams.get("visitors", {}).get("name", "?")
        home_pts = scores.get("home", {}).get("points", "?")
        vis_pts = scores.get("visitors", {}).get("points", "?")
        lines.append("")
        lines.append(f"  {vis_name} {vis_pts} @ {home_name} {home_pts}")
    return "\n".join(lines)


def main() -> None:
    date_str = input("Date (YYYY-MM-DD, blank for yesterday): ").strip() or None
    client = NBAClient()
    games = fetch_games(client, date_str)
    summary = _format_summary(games, date_str or "yesterday")
    sender = ConsoleSender()
    sender.send("NBA Results", summary)


if __name__ == "__main__":
    main()
