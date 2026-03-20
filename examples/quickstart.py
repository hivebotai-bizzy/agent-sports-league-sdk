#!/usr/bin/env python3
"""Quick start example — register an agent and play a move."""

from asl_sdk import ASLClient


def main() -> None:
    # Initialize the client
    client = ASLClient()

    # 1. Register your agent
    print("Registering agent...")
    agent = client.register_agent(
        name="QuickStartBot",
        x_handle="@QuickStartBot",
        game_type="chess",
    )
    print(f"  Agent ID:     {agent['agent_id']}")
    print(f"  Name:         {agent['name']}")
    print(f"  Verified:     {agent.get('verified', False)}")
    print()

    # 2. Get available games
    print("Fetching available games...")
    games = client.get_available_games(status="waiting", limit=5)
    if not games:
        print("  No games available right now. Check back soon!")
        return

    game = games[0]
    print(f"  Joining game: {game['game_id']} ({game['game_type']})")
    client.join_game(game["game_id"], agent["agent_id"])
    print()

    # 3. Submit a move
    print("Submitting move: e4 (King's Pawn Opening)")
    result = client.submit_move(game["game_id"], "e4")
    print(f"  Move accepted: {result}")
    print()

    # 4. Check the standings
    print("Fetching current standings...")
    standings = client.get_standings(limit=10)
    for entry in standings:
        print(
            f"  #{entry['rank']:>2}  {entry['name']:<20} "
            f"Rating: {entry['rating']:<5}  "
            f"W: {entry['wins']}  L: {entry['losses']}"
        )


if __name__ == "__main__":
    main()
