"""API class to fetch yield curve data from AlphaVantage endpoints."""

import asyncio

import aiohttp


class AsyncDataAPI:
    """
    API class to fetch yield curve data async from AlphaVantage API.

    :param api_key: AlphaVantage API key available at https://www.alphavantage.co/support/#api-key
    :param interval: Interval for data being retrieved (i.e. daily, weekly, or monthly).
    """

    def __init__(self, api_key, interval):
        self.base_url = "https://www.alphavantage.co/query?"
        self.api_key = api_key
        self.interval = interval

    async def get_data(self, endpoint, params=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                response.raise_for_status()

    async def get_yields(self, interval: str = "daily") -> dict:

        if interval not in {"daily", "weekly", "monthly"}:
            raise ValueError("Interval value must be one of: 'daily', 'weekly', 'monthly'")

        endpoints = {
            "FedFunds": f"function=FEDERAL_FUNDS_RATE&interval={self.interval}&apikey={self.api_key}",
            "3month": f"function=TREASURY_YIELD&interval={self.interval}&maturity=3month&apikey={self.api_key}",
            "2year": f"function=TREASURY_YIELD&interval={self.interval}&maturity=2year&apikey={self.api_key}",
            "5year": f"function=TREASURY_YIELD&interval={self.interval}&maturity=5year&apikey={self.api_key}",
            "7year": f"function=TREASURY_YIELD&interval={self.interval}&maturity=7year&apikey={self.api_key}",
            "10year": f"function=TREASURY_YIELD&interval={self.interval}&maturity=10year&apikey={self.api_key}",
            "30year": f"function=TREASURY_YIELD&interval={self.interval}&maturity=30year&apikey={self.api_key}",
        }

        tasks = [self.get_data(endpoint) for endpoint in endpoints.values()]
        responses = await asyncio.gather(*tasks)

        return {
            "FedFunds": responses[0],
            "3month": responses[1],
            "2year": responses[2],
            "5year": responses[3],
            "7year": responses[4],
            "10year": responses[5],
            "30year": responses[6],
        }
