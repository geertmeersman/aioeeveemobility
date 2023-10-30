"""EEVEE Mobility library using aiohttp."""
from __future__ import annotations

import aiohttp
from datetime import datetime
import time
from .const import TOKEN_URL, API_URL, CLIENT_ID, CLIENT_SECRET, HEADERS

class EeveeMobilityClient:
    """Class to communicate with the EEVEE Mobility API."""

    def __init__(
        self, email, password, custom_headers=None
    ):
        """Initialize the API to get data."""
        self.email = email
        self.password = password
        self.token = None
        self.session = None
        self.custom_headers = custom_headers or {}

    async def start_session(self):
        """Start the aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.custom_headers)

    async def close_session(self):
        """Close the session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_token(self, force=False):
        """Get the OAuth token."""
        if self.token is None or force is True:
            async with self.session.post(
                TOKEN_URL,
                data={
                    "grant_type": "password",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "username": self.email,
                    "password": self.password,
                },
            ) as response:
                token_info = await response.json()
            self.token = token_info
        return self.token["access_token"]

    async def request(self, path):
        """Send an authorized request to an API endpoint."""
        if self.session is None:
            await self.start_session()

        endpoint_path = f"{API_URL}/{path}"
        token = await self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        headers.update(HEADERS)
        headers.update(self.custom_headers)

        async with self.session.get(endpoint_path, headers=headers) as response:
            if response.status == 401:
                token = await self.get_token(True)
                headers["Authorization"] = f"Bearer {token}"
                async with self.session.get(endpoint_path, headers=headers) as refreshed_response:
                    if refreshed_response.status == 200:
                        return await refreshed_response.json()
                    else:
                        raise Exception(f"Failed to refresh token and access {endpoint_path}")
            elif response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Request to {endpoint_path} failed with status code {response.status}")
