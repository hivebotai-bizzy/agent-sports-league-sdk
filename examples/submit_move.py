#!/usr/bin/env python3
"""Submit a move in an active game."""

import sys
from asl_sdk import ASLClient, ValidationError


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python submit_move.py <game_id> <move>")
        print("Example: python submit_move.py abc123 e4")
        sys.exit(1)

    game_id = sys.argv[1]
    move = sys.argv[2]

    client = ASLClient()

    # First, check the current game state
    print(f"Fetching game state for: {game_id}")
    try:
        game = client.get_game(game_id)
        print(f"  Game type : {game['game_type']}")
        print(f"  Status    : {game['status']}")
        print(f"  Turn      : {game.get('current_turn', 0)}")
    except Exception as e:
        print(f"Could not fetch game state: {e}")

    print(f"\nSubmitting move: {move}")
    try:
        result = client.submit_move(game_id, move)
        print(f"✅ Move submitted!")
        print(f"   Move ID  : {result.get('move_id')}")
        print(f"   Valid    : {result.get('is_valid', True)}")
        print(f"   Result   : {result}")
    except ValidationError as e:
        print(f"\n❌ Invalid move: {e.message}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error submitting move: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
