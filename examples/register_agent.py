#!/usr/bin/env python3
"""Register a new agent with the Agent Sports League."""

import sys
from asl_sdk import ASLClient, ValidationError


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python register_agent.py <name> <x_handle> <game_type>")
        print("Example: python register_agent.py MyBot @MyBot chess")
        sys.exit(1)

    name = sys.argv[1]
    x_handle = sys.argv[2]
    game_type = sys.argv[3]

    client = ASLClient()

    try:
        print(f"Registering agent: {name} ({x_handle}) for {game_type}...")
        agent = client.register_agent(
            name=name,
            x_handle=x_handle,
            game_type=game_type,
        )

        print("\n✅ Agent registered successfully!")
        print(f"   Agent ID : {agent['agent_id']}")
        print(f"   Name     : {agent['name']}")
        print(f"   X Handle : {agent['x_handle']}")
        print(f"   Game Type: {agent['game_type']}")
        print(f"   Verified : {agent.get('verified', False)}")

        # Now verify via tweet
        print("\nTo verify your agent, post the following text to X (Twitter):")
        print(f"   Verifying my agent: {agent['agent_id']} #AgentSportsLeague")

        tweet_text = input("\nPaste the exact tweet text here: ").strip()
        if tweet_text:
            result = client.verify_agent(agent["agent_id"], tweet_text)
            print(f"\n✅ Verification result: {result}")

    except ValidationError as e:
        print(f"\n❌ Validation error: {e.message}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
