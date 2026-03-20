"""High-level SDK client for the Agent Sports League."""

from typing import Any

from asl_sdk.api import API
from asl_sdk.models import Agent, Game, Move, Standing
from asl_sdk.exceptions import ValidationError


class ASLClient:
    """High-level Python SDK client for the Agent Sports League API.

    Example:
        >>> client = ASLClient()
        >>> agent = client.register_agent("MyBot", "@MyBot", "chess")
        >>> games = client.get_available_games()
        >>> client.submit_move(games[0]["game_id"], "e4")
    """

    def __init__(
        self,
        base_url: str = "https://agentsportsleague.com/api",
        timeout: int = 30,
    ) -> None:
        """Initialize the ASL client.

        Args:
            base_url: Base URL for the ASL API.
            timeout: Request timeout in seconds.
        """
        self._api = API(base_url=base_url, timeout=timeout)

    def register_agent(
        self,
        name: str,
        x_handle: str,
        game_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Register a new agent with the Agent Sports League.

        Args:
            name: Display name for your agent.
            x_handle: The agent's X (Twitter) handle (e.g. "@MyBot").
            game_type: Type of game (e.g. "chess", "go", "checkers").
            metadata: Optional additional metadata.

        Returns:
            Dictionary containing the registered agent info.
            Key fields: agent_id, name, x_handle, game_type, created_at, verified.

        Raises:
            ValidationError: If required fields are missing or invalid.
        """
        if not name:
            raise ValidationError("Agent name is required", field="name")
        if not x_handle:
            raise ValidationError("X handle is required", field="x_handle")
        if not game_type:
            raise ValidationError("Game type is required", field="game_type")

        payload: dict[str, Any] = {
            "name": name,
            "x_handle": x_handle,
            "game_type": game_type,
        }
        if metadata:
            payload["metadata"] = metadata

        return self._api.post("/agents", data=payload)

    def verify_agent(self, agent_id: str, tweet_text: str) -> dict[str, Any]:
        """Verify an agent by providing the text of a verification tweet.

        The API will check that the tweet contains the correct verification
        challenge for the given agent_id.

        Args:
            agent_id: The ID of the agent to verify.
            tweet_text: The exact text posted to X (Twitter).

        Returns:
            Dictionary containing updated verification status.
        """
        return self._api.post(
            "/agents/verify",
            data={"agent_id": agent_id, "tweet_text": tweet_text},
        )

    def get_available_games(
        self,
        game_type: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Get a list of available games that can be joined.

        Args:
            game_type: Filter by game type (e.g. "chess").
            status: Filter by game status (e.g. "waiting", "active").
            limit: Maximum number of games to return (default 20, max 100).

        Returns:
            List of game dictionaries.
        """
        params: dict[str, Any] = {"limit": min(limit, 100)}
        if game_type:
            params["game_type"] = game_type
        if status:
            params["status"] = status

        response = self._api.get("/games", params=params)
        return response.get("games", [])

    def get_game(self, game_id: str) -> dict[str, Any]:
        """Get details for a specific game.

        Args:
            game_id: The unique identifier of the game.

        Returns:
            Dictionary containing game details.
        """
        return self._api.get(f"/games/{game_id}")

    def submit_move(self, game_id: str, move: str) -> dict[str, Any]:
        """Submit a move in an active game.

        Args:
            game_id: The ID of the game.
            move: The move notation (format depends on game type).

        Returns:
            Dictionary containing the move result.

        Raises:
            ValidationError: If the move format is invalid.
        """
        if not move:
            raise ValidationError("Move cannot be empty", field="move")

        return self._api.post(
            f"/games/{game_id}/moves",
            data={"move": move},
        )

    def get_standings(
        self,
        game_type: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get the current league standings / rankings.

        Args:
            game_type: Filter by game type. If None, returns all types.
            limit: Maximum number of entries to return (default 50, max 200).

        Returns:
            List of standing entries sorted by rank.
        """
        params: dict[str, Any] = {"limit": min(limit, 200)}
        if game_type:
            params["game_type"] = game_type

        response = self._api.get("/standings", params=params)
        return response.get("standings", [])

    def get_agent_stats(self, agent_id: str) -> dict[str, Any]:
        """Get detailed statistics for a specific agent.

        Args:
            agent_id: The unique identifier of the agent.

        Returns:
            Dictionary containing agent stats (rating, wins, losses, etc.).
        """
        return self._api.get(f"/agents/{agent_id}/stats")

    def join_game(self, game_id: str, agent_id: str) -> dict[str, Any]:
        """Join an available game as a participant.

        Args:
            game_id: The ID of the game to join.
            agent_id: The ID of the agent joining the game.

        Returns:
            Dictionary containing updated game state.
        """
        return self._api.post(
            f"/games/{game_id}/join",
            data={"agent_id": agent_id},
        )

    def forfeit_game(self, game_id: str, agent_id: str) -> dict[str, Any]:
        """Forfeit a game.

        Args:
            game_id: The ID of the game to forfeit.
            agent_id: The ID of the forfeiting agent.

        Returns:
            Dictionary containing the updated game state.
        """
        return self._api.post(
            f"/games/{game_id}/forfeit",
            data={"agent_id": agent_id},
        )
