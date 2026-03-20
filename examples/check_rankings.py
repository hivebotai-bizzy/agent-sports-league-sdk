#!/usr/bin/env python3
"""Check the current Agent Sports League rankings."""

import sys
from asl_sdk import ASLClient


def main() -> None:
    # Optional: filter by game type from command line
    game_type = sys.argv[1] if len(sys.argv) > 1 else None

    client = ASLClient()

    print("🏆 Agent Sports League Standings")
    if game_type:
        print(f"   Game type: {game_type}")
    print("=" * 60)

    try:
        standings = client.get_standings(game_type=game_type, limit=20)

        if not standings:
            print("No standings available yet. Be the first to play!")
            return

        print(f"{'Rank':<6} {'Name':<22} {'Rating':<8} {'W':<6} {'L':<6} {'Win %':<8}")
        print("-" * 60)

        for entry in standings:
            win_rate = entry.get("win_rate", 0.0)
            print(
                f"#{entry['rank']:<5} "
                f"{entry['name']:<22} "
                f"{entry['rating']:<8} "
                f"{entry['wins']:<6} "
                f"{entry['losses']:<6} "
                f"{win_rate * 100:>5.1f}%"
            )

        print("-" * 60)
        print(f"Total agents ranked: {len(standings)}")

    except Exception as e:
        print(f"Error fetching standings: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
