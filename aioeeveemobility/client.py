"""EEVEE Mobility library using aiohttp."""
import aiohttp

from .const import API_URL, CLIENT_ID, CLIENT_SECRET, HEADERS, TOKEN_URL


class EeveeMobilityClient:
    """Class to communicate with the EEVEE Mobility API."""

    def __init__(self, email, password, custom_headers=None):
        """Initialize the EEVEE Mobility Client.

        Args:
        ----
            email (str): Email associated with the EEVEE Mobility account.
            password (str): Password for the EEVEE Mobility account.
            custom_headers (dict, optional): Custom headers to be included in requests. Defaults to None.

        """
        self.email = email
        self.password = password
        self.token = None
        self.session = None
        self.custom_headers = custom_headers or {}

    async def _start_session(self):
        """Start an aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.custom_headers)

    async def _close_session(self):
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def _get_token(self, force=False):
        """Obtain the OAuth token."""
        if self.token is None or force:
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
        return self.token.get("access_token")

    async def request(self, path):
        """Send an authorized request to an API endpoint.

        Args:
        ----
            path (str): The endpoint path to send the request to.

        Returns:
        -------
            dict: JSON response from the API.

        Raises:
        ------
            EeveeAPIException: If the request fails or authentication issues occur.

        """
        await self._start_session()

        endpoint_path = f"{API_URL}/{path}"
        token = await self._get_token()
        headers = {"Authorization": f"Bearer {token}"}
        headers.update(HEADERS)
        headers.update(self.custom_headers)

        async with self.session.get(endpoint_path, headers=headers) as response:
            if response.status == 401:
                token = await self._get_token(force=True)
                headers["Authorization"] = f"Bearer {token}"
                async with self.session.get(
                    endpoint_path, headers=headers
                ) as refreshed_response:
                    if refreshed_response.status == 200:
                        return await refreshed_response.json()
                    else:
                        raise EeveeAPIException(
                            f"Failed to refresh token and access {endpoint_path}"
                        )
            elif response.status == 200:
                return await response.json()
            else:
                raise EeveeAPIException(
                    f"Request to {endpoint_path} failed with status code {response.status}"
                )


class EeveeAPIException(Exception):
    """Exception raised for errors in the EEVEE Mobility API."""

    def __init__(self, message):
        """Initialize the EeveeAPIException.

        Args:
        ----
            message (str): The error message.

        """
        self.message = message
        super().__init__(self.message)
