"""Low-level API client for the ASL REST API."""

import requests
from typing import Any

from asl_sdk.exceptions import (
    ASLException,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    APIError,
)


class API:
    """Low-level API client for making requests to the ASL API."""

    def __init__(
        self,
        base_url: str = "https://agentsportsleague.com/api",
        timeout: int = 30,
    ) -> None:
        """Initialize the API client.

        Args:
            base_url: Base URL for the API. Defaults to the production ASL API.
            timeout: Request timeout in seconds. Defaults to 30.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            endpoint: API endpoint path.
            data: JSON request body.
            params: URL query parameters.
            headers: Additional HTTP headers.

        Returns:
            Parsed JSON response.

        Raises:
            ASLException: On API errors.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)

        try:
            response = self._session.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            raise ASLException(f"Request failed: {e}")

        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        """Handle an HTTP response and parse JSON.

        Args:
            response: The requests Response object.

        Returns:
            Parsed JSON response.

        Raises:
            ASLException: On API errors.
        """
        status_code = response.status_code

        if status_code == 200 or status_code == 201:
            return response.json()

        if status_code == 400:
            try:
                body = response.json()
                message = body.get("message", "Validation error")
                field = body.get("field")
            except Exception:
                message = "Validation error"
                field = None
            raise ValidationError(message, field=field)

        if status_code == 401:
            raise AuthenticationError("Invalid or missing credentials")

        if status_code == 404:
            try:
                body = response.json()
                message = body.get("message", "Resource not found")
            except Exception:
                message = "Resource not found"
            raise NotFoundError(message)

        if status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                "Rate limit exceeded. Please slow down.",
                retry_after=int(retry_after) if retry_after else None,
            )

        try:
            body = response.json()
            message = body.get("message", f"API error (status {status_code})")
        except Exception:
            message = f"API error (status {status_code})"

        raise APIError(message, status_code=status_code)

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request."""
        return self._request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a POST request."""
        return self._request("POST", endpoint, data=data)

    def put(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a PUT request."""
        return self._request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Make a DELETE request."""
        return self._request("DELETE", endpoint)
