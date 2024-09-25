"""API class to fetch yield curve data from AlphaVantage endpoints."""

import asyncio

import aiohttp


class AsyncDataAPI:
    """
    Wrapper around AlphaVantageAPI to fetch historical treasury data.
    """

    def __init__(self, api_key):
        self.base_url = "https://www.alphavantage.co/query?"
        self.api_key = api_key
        self.yc_data = None

    async def get_data(self, endpoint, params=None):
        """
        Fetches data from the specified endpoint of the AlphaVantage API.

        Args:
            endpoint (str): The specific API endpoint to fetch data from.
            params (dict, optional): Additional parameters to include in the request.

        Returns:
            dict: The JSON response from the API if the request is successful.

        Raises:
            aiohttp.ClientResponseError: If the response status is not 200.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()

    async def get_yields(self, interval: str = "daily"):
        """
        Fetches yield data for various yield maturities from the AlphaVantage API.

        Args:
            interval (str): The interval for the yield data. Must be one of 'daily', 'weekly', or 'monthly'.

        Raises:
            ValueError: If the provided interval is not one of the allowed values.

        Returns:
            None: The method populates the instance variable `yc_data` with the fetched yield data.
        """
        if interval not in {"daily", "weekly", "monthly"}:
            raise ValueError("Interval value must be one of: 'daily', 'weekly', 'monthly'")

        # dict of endpoints we will hit for historical data
        endpoints = {
            "FedFunds": f"function=FEDERAL_FUNDS_RATE&interval={interval}&apikey={self.api_key}",
            "3month": f"function=TREASURY_YIELD&interval={interval}&maturity=3month&apikey={self.api_key}",
            "2year": f"function=TREASURY_YIELD&interval={interval}&maturity=2year&apikey={self.api_key}",
            "5year": f"function=TREASURY_YIELD&interval={interval}&maturity=5year&apikey={self.api_key}",
            "7year": f"function=TREASURY_YIELD&interval={interval}&maturity=7year&apikey={self.api_key}",
            "10year": f"function=TREASURY_YIELD&interval={interval}&maturity=10year&apikey={self.api_key}",
            "30year": f"function=TREASURY_YIELD&interval={interval}&maturity=30year&apikey={self.api_key}",
        }

        # retrieve data from API and save to class attribute
        tasks = [self.get_data(endpoint) for endpoint in endpoints.values()]
        responses = await asyncio.gather(*tasks)
        self.yc_data = {
            "FedFunds": responses[0],
            "3month": responses[1],
            "2year": responses[2],
            "5year": responses[3],
            "7year": responses[4],
            "10year": responses[5],
            "30year": responses[6],
        }
