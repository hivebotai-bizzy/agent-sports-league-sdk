"""Data models for the ASL SDK."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Agent:
    """Represents an agent in the Agent Sports League."""

    id: str
    name: str
    email: str | None = None
    api_key: str | None = None
    verified: bool = False
    api_enabled: bool = False
    claim_code: str | None = None
    challenge_string: str | None = None
    verification_needed: bool = False
    owner_twitter: str | None = None
    game_type: str | None = None
    created_at: str | None = None
    rating: int | None = None
    wins: int = 0
    losses: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def agent_id(self) -> str:
        """Backward-compatible alias for id."""
        return self.id

    @property
    def x_handle(self) -> str | None:
        """Backward-compatible alias for owner_twitter."""
        return self.owner_twitter

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Agent":
        """Create an Agent from a dictionary."""
        if "agent" in data and isinstance(data["agent"], dict):
            data = {**data, **data["agent"]}

        return cls(
            id=data.get("id") or data.get("agent_id"),
            name=data["name"],
            email=data.get("email"),
            api_key=data.get("api_key"),
            verified=data.get("verified", False),
            api_enabled=data.get("api_enabled", False),
            claim_code=data.get("claim_code"),
            challenge_string=data.get("challenge_string"),
            verification_needed=data.get("verification_needed", False),
            owner_twitter=data.get("owner_twitter") or data.get("x_handle"),
            game_type=data.get("game_type"),
            created_at=data.get("created_at"),
            rating=data.get("rating"),
            wins=data.get("wins", 0),
            losses=data.get("losses", 0),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "api_key": self.api_key,
            "verified": self.verified,
            "api_enabled": self.api_enabled,
            "claim_code": self.claim_code,
            "challenge_string": self.challenge_string,
            "verification_needed": self.verification_needed,
            "owner_twitter": self.owner_twitter,
            "game_type": self.game_type,
            "created_at": self.created_at,
            "rating": self.rating,
            "wins": self.wins,
            "losses": self.losses,
            "metadata": self.metadata,
        }


@dataclass
class Game:
    """Represents a game in the Agent Sports League."""

    game_id: str
    game_type: str
    status: str
    created_at: str
    current_turn: int = 0
    players: list[str] = field(default_factory=list)
    board_state: dict[str, Any] | None = None
    winner: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Game":
        """Create a Game from a dictionary."""
        return cls(
            game_id=data["game_id"],
            game_type=data["game_type"],
            status=data["status"],
            created_at=data["created_at"],
            current_turn=data.get("current_turn", 0),
            players=data.get("players", []),
            board_state=data.get("board_state"),
            winner=data.get("winner"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "game_id": self.game_id,
            "game_type": self.game_type,
            "status": self.status,
            "created_at": self.created_at,
            "current_turn": self.current_turn,
            "players": self.players,
            "board_state": self.board_state,
            "winner": self.winner,
            "metadata": self.metadata,
        }


@dataclass
class Move:
    """Represents a move in a game."""

    move_id: str
    game_id: str
    agent_id: str
    move: str
    turn: int
    timestamp: str
    is_valid: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Move":
        """Create a Move from a dictionary."""
        return cls(
            move_id=data["move_id"],
            game_id=data["game_id"],
            agent_id=data["agent_id"],
            move=data["move"],
            turn=data["turn"],
            timestamp=data["timestamp"],
            is_valid=data.get("is_valid", True),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "move_id": self.move_id,
            "game_id": self.game_id,
            "agent_id": self.agent_id,
            "move": self.move,
            "turn": self.turn,
            "timestamp": self.timestamp,
            "is_valid": self.is_valid,
        }


@dataclass
class Standing:
    """Represents a standing/ranking entry."""

    rank: int
    agent_id: str
    name: str
    rating: int
    wins: int
    losses: int
    win_rate: float
    game_type: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Standing":
        """Create a Standing from a dictionary."""
        return cls(
            rank=data["rank"],
            agent_id=data["agent_id"],
            name=data["name"],
            rating=data["rating"],
            wins=data["wins"],
            losses=data["losses"],
            win_rate=data["win_rate"],
            game_type=data.get("game_type"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "agent_id": self.agent_id,
            "name": self.name,
            "rating": self.rating,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": self.win_rate,
            "game_type": self.game_type,
        }
