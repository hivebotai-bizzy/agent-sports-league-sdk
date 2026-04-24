"""Tests for the ASL SDK client."""

import hashlib
import hmac
import pytest
from unittest.mock import patch, MagicMock

from asl_sdk import ASLClient, ValidationError
from asl_sdk.api import API
from asl_sdk.exceptions import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    APIError,
)


class TestASLClient:
    """Tests for ASLClient."""

    @pytest.fixture
    def client(self) -> ASLClient:
        """Create a client with a mocked API."""
        with patch.object(API, "__init__", return_value=None):
            c = ASLClient()
            c._api = MagicMock(spec=API)
            return c

    def test_register_agent_success(self, client: ASLClient) -> None:
        """Test successful agent registration."""
        mock_response = {
            "id": "agt_123",
            "name": "TestBot",
            "claim_code": "claim_123",
            "challenge_string": "challenge_abc",
            "api_key": "key_123",
            "verification_needed": True,
            "game_type": "chess",
            "verified": False,
        }
        client._api.post.return_value = mock_response

        result = client.register_agent("TestBot", "@TestBot", "chess")

        assert result["id"] == "agt_123"
        assert result["name"] == "TestBot"
        assert client.api_key == "key_123"
        assert client.challenge_string == "challenge_abc"
        client._api.post.assert_called_once_with(
            "/agents/register",
            data={
                "name": "TestBot",
                "owner_twitter": "@TestBot",
                "game_type": "chess",
            },
        )

    def test_register_agent_missing_name(self, client: ASLClient) -> None:
        """Test registration fails without a name."""
        with pytest.raises(ValidationError) as exc_info:
            client.register_agent("", "@TestBot", "chess")
        assert exc_info.value.field == "name"

    def test_register_agent_missing_x_handle(self, client: ASLClient) -> None:
        """Test registration fails without an X handle."""
        with pytest.raises(ValidationError) as exc_info:
            client.register_agent("TestBot", "", "chess")
        assert exc_info.value.field == "owner_twitter"

    def test_register_agent_missing_game_type(self, client: ASLClient) -> None:
        """Test registration fails without a game type."""
        with pytest.raises(ValidationError) as exc_info:
            client.register_agent("TestBot", "@TestBot", "")
        assert exc_info.value.field == "game_type"

    def test_verify_agent(self, client: ASLClient) -> None:
        """Test HMAC agent verification."""
        mock_response = {
            "id": "agt_123",
            "api_key": "key_123",
            "verified": True,
            "api_enabled": True,
        }
        client._api.post.return_value = mock_response
        client.challenge_string = "challenge_abc"

        result = client.verify_agent("claim_123", "key_123")

        assert result["verified"] is True
        expected_signature = hmac.new(
            b"key_123",
            b"challenge_abc",
            hashlib.sha256,
        ).hexdigest()
        client._api.post.assert_called_once_with(
            "/agents/verify",
            data={
                "claim_code": "claim_123",
                "api_key": "key_123",
                "challenge_string": "challenge_abc",
                "signed_challenge": expected_signature,
            },
        )

    def test_get_current_agent(self, client: ASLClient) -> None:
        """Test fetching the authenticated agent."""
        client._api.get.return_value = {"id": "agt_123", "name": "TestBot"}

        result = client.get_current_agent(api_key="key_123")

        assert result["id"] == "agt_123"
        client._api.get.assert_called_once_with(
            "/agents/me", headers={"X-ASL-Key": "key_123"}
        )

    def test_get_available_games(self, client: ASLClient) -> None:
        """Test fetching available games."""
        mock_response = {
            "games": [
                {"game_id": "gm_abc", "game_type": "chess", "status": "waiting"}
            ]
        }
        client._api.get.return_value = mock_response

        games = client.get_available_games(game_type="chess", limit=10)

        assert len(games) == 1
        assert games[0]["game_id"] == "gm_abc"
        client._api.get.assert_called_once_with(
            "/games", params={"limit": 10, "game_type": "chess"}
        )

    def test_get_game(self, client: ASLClient) -> None:
        """Test fetching a specific game."""
        mock_response = {
            "game_id": "gm_abc",
            "game_type": "chess",
            "status": "active",
        }
        client._api.get.return_value = mock_response

        game = client.get_game("gm_abc")

        assert game["game_id"] == "gm_abc"
        client._api.get.assert_called_once_with("/games/gm_abc")

    def test_submit_move_success(self, client: ASLClient) -> None:
        """Test submitting a valid move."""
        mock_response = {
            "move_id": "mv_1",
            "game_id": "gm_abc",
            "is_valid": True,
        }
        client._api.post.return_value = mock_response
        client.api_key = "key_123"

        result = client.submit_move("gm_abc", "e4")

        assert result["is_valid"] is True
        client._api.post.assert_called_once_with(
            "/games/gm_abc/submit",
            data={"move": "e4"},
            headers={"X-ASL-Key": "key_123"},
        )

    def test_submit_move_empty(self, client: ASLClient) -> None:
        """Test submitting an empty move raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            client.submit_move("gm_abc", "")
        assert exc_info.value.field == "move"

    def test_get_standings(self, client: ASLClient) -> None:
        """Test fetching standings."""
        mock_response = {
            "standings": [
                {"rank": 1, "name": "AlphaZero", "rating": 1800}
            ]
        }
        client._api.get.return_value = mock_response

        standings = client.get_standings(limit=10)

        assert len(standings) == 1
        assert standings[0]["rank"] == 1
        client._api.get.assert_called_once_with(
            "/standings", params={"limit": 10}
        )

    def test_get_agent_stats(self, client: ASLClient) -> None:
        """Test fetching agent stats."""
        mock_response = {
            "agent_id": "agt_123",
            "rating": 1500,
            "wins": 10,
            "losses": 2,
        }
        client._api.get.return_value = mock_response

        stats = client.get_agent_stats("agt_123")

        assert stats["wins"] == 10
        client._api.get.assert_called_once_with("/agents/agt_123/stats")

    def test_join_game(self, client: ASLClient) -> None:
        """Test joining a game."""
        mock_response = {
            "game_id": "gm_abc",
            "status": "active",
            "players": ["agt_123", "agt_456"],
        }
        client._api.post.return_value = mock_response

        result = client.join_game("gm_abc", "agt_123")

        assert "agt_123" in result["players"]
        client._api.post.assert_called_once_with(
            "/games/gm_abc/join", data={"agent_id": "agt_123"}
        )

    def test_forfeit_game(self, client: ASLClient) -> None:
        """Test forfeiting a game."""
        mock_response = {
            "game_id": "gm_abc",
            "status": "completed",
            "winner": "agt_456",
        }
        client._api.post.return_value = mock_response

        result = client.forfeit_game("gm_abc", "agt_123")

        assert result["status"] == "completed"
        client._api.post.assert_called_once_with(
            "/games/gm_abc/forfeit", data={"agent_id": "agt_123"}
        )


class TestAPIExceptions:
    """Tests for API exception handling."""

    @pytest.fixture
    def api(self) -> API:
        """Create an API instance targeting a test server."""
        with patch("requests.Session"):
            return API(base_url="https://test.agentsportsleague.com/api")

    def test_validation_error(self, api: API) -> None:
        """Test ValidationError is raised on 400."""
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {"message": "Name required", "field": "name"}

        with pytest.raises(ValidationError) as exc_info:
            api._handle_response(response)
        assert exc_info.value.message == "Name required"
        assert exc_info.value.field == "name"

    def test_authentication_error(self, api: API) -> None:
        """Test AuthenticationError is raised on 401."""
        response = MagicMock()
        response.status_code = 401
        response.json.return_value = {"message": "Invalid token"}

        with pytest.raises(AuthenticationError):
            api._handle_response(response)

    def test_not_found_error(self, api: API) -> None:
        """Test NotFoundError is raised on 404."""
        response = MagicMock()
        response.status_code = 404
        response.json.return_value = {"message": "Game not found"}

        with pytest.raises(NotFoundError) as exc_info:
            api._handle_response(response)
        assert exc_info.value.message == "Game not found"

    def test_rate_limit_error(self, api: API) -> None:
        """Test RateLimitError is raised on 429."""
        response = MagicMock()
        response.status_code = 429
        response.headers = {"Retry-After": "60"}
        response.json.return_value = {"message": "Slow down"}

        with pytest.raises(RateLimitError) as exc_info:
            api._handle_response(response)
        assert exc_info.value.retry_after == 60

    def test_api_error(self, api: API) -> None:
        """Test APIError is raised on unexpected status codes."""
        response = MagicMock()
        response.status_code = 500
        response.json.return_value = {"message": "Internal server error"}

        with pytest.raises(APIError) as exc_info:
            api._handle_response(response)
        assert exc_info.value.status_code == 500
