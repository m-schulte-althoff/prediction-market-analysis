"""Small retrying client for public, read-only JSON endpoints."""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

LOGGER = logging.getLogger(__name__)


class PublicApiClient:
    """Retrieve JSON with bounded retries and an identifying user agent."""

    def __init__(self, timeout_seconds: int = 45, retries: int = 4) -> None:
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "prediction-market-semantic-study/0.1 (academic research)"}
        )

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        """Return parsed JSON, retrying transient HTTP and connection failures."""

        for attempt in range(self.retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout_seconds,
                )
                if 400 <= response.status_code < 500 and response.status_code != 429:
                    raise RuntimeError(
                        f"Public API rejected request {response.url}: "
                        f"{response.status_code} {response.text[:300]}"
                    )
                response.raise_for_status()
                return response.json()
            except RuntimeError:
                raise
            except (requests.RequestException, ValueError) as error:
                if attempt == self.retries - 1:
                    detail = ""
                    if isinstance(error, requests.HTTPError) and error.response is not None:
                        detail = f" {error.response.status_code} {error.response.text[:300]}"
                    raise RuntimeError(f"Public API request failed: {url}.{detail}") from error
                delay = 0.75 * (2**attempt)
                LOGGER.warning("Request failed; retrying in %.2fs: %s", delay, url)
                time.sleep(delay)
        raise AssertionError("unreachable")
