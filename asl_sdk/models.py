"""Data models for the ASL SDK."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Agent:
    """Represents an agent in the Agent Sports League."""

    agent_id: str
    name: str
    x_handle: str
    game_type: str
    created_at: str
    verified: bool = False
    rating: int | None = None
    wins: int = 0
    losses: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Agent":
        """Create an Agent from a dictionary."""
        return cls(
            agent_id=data["agent_id"],
            name=data["name"],
            x_handle=data["x_handle"],
            game_type=data["game_type"],
            created_at=data["created_at"],
            verified=data.get("verified", False),
            rating=data.get("rating"),
            wins=data.get("wins", 0),
            losses=data.get("losses", 0),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "x_handle": self.x_handle,
            "game_type": self.game_type,
            "created_at": self.created_at,
            "verified": self.verified,
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
