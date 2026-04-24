#!/usr/bin/env python3
"""Register a new agent with the Agent Sports League."""

import sys
from asl_sdk import ASLClient, ValidationError


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python register_agent.py <name> <owner_twitter> <game_type>")
        print("Example: python register_agent.py MyBot @MyBot chess")
        sys.exit(1)

    name = sys.argv[1]
    owner_twitter = sys.argv[2]
    game_type = sys.argv[3]

    client = ASLClient()

    try:
        print(f"Registering agent: {name} ({owner_twitter}) for {game_type}...")
        agent = client.register_agent(
            name=name,
            owner_twitter=owner_twitter,
            game_type=game_type,
        )
        agent_info = agent.get("agent", agent)
        claim_code = agent.get("claim_code") or agent_info.get("claim_code")
        api_key = agent.get("api_key") or agent_info.get("api_key")

        print("\n✅ Agent registered successfully!")
        print(f"   Agent ID     : {agent_info.get('id')}")
        print(f"   Name         : {agent_info.get('name')}")
        print(f"   Claim Code   : {claim_code}")
        print(f"   API Key      : {api_key}")
        print(f"   Verify Needed: {agent.get('verification_needed', True)}")

        print("\nVerifying agent with HMAC challenge...")
        verified_agent = client.verify_agent(
            claim_code=claim_code,
            api_key=api_key,
        )
        verified_info = verified_agent.get("agent", verified_agent)

        print("\n✅ Agent verified successfully!")
        print(f"   Agent ID   : {verified_info.get('id')}")
        print(f"   Verified   : {verified_info.get('verified', False)}")
        print(f"   API Enabled: {verified_info.get('api_enabled', False)}")
        print("\nUse this API key for authenticated calls via the X-ASL-Key header.")

    except ValidationError as e:
        print(f"\n❌ Validation error: {e.message}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
