"""API class to fetch yield curve data from AlphaVantage endpoints."""

import asyncio

import aiohttp


def get_historical_yield_data_endpoints(interval: str, api_key: str) -> dict:
    """
    Return dict of API endpoints for given time interval and API key.

    Args
    ----
        interval (str): Specify the interval for the yield data.
        - Must be one of 'daily', 'weekly', or 'monthly'.
        api_key (str): API key for AlphaVantageAPI.

    Returns
    -------
        dict: Dictionary of API endpoints to hit for historical data.

    """
    return {
        "FedFunds": f"function=FEDERAL_FUNDS_RATE&interval={interval}&apikey={api_key}",
        "3month": f"function=TREASURY_YIELD&interval={interval}&maturity=3month&apikey={api_key}",
        "2year": f"function=TREASURY_YIELD&interval={interval}&maturity=2year&apikey={api_key}",
        "5year": f"function=TREASURY_YIELD&interval={interval}&maturity=5year&apikey={api_key}",
        "7year": f"function=TREASURY_YIELD&interval={interval}&maturity=7year&apikey={api_key}",
        "10year": f"function=TREASURY_YIELD&interval={interval}&maturity=10year&apikey={api_key}",
        "30year": f"function=TREASURY_YIELD&interval={interval}&maturity=30year&apikey={api_key}",
    }


class AsyncDataAPI:
    """Wrapper around AlphaVantageAPI to fetch historical treasury data."""

    def __init__(self, api_key):
        self.base_url = "https://www.alphavantage.co/query?"
        self.api_key = api_key
        self.yc_data = None
        self.economic_data = None

        # dict of endpoints we will hit for historical data

    async def get_data(self, endpoint, params=None):
        """
        Fetch data from the specified endpoint of the AlphaVantage API.

        Args
        ----
            endpoint (str): API endpoint to fetch data from.
            params (dict, optional): Additional parameters to include in the request.

        Returns
        -------
            dict: Return the JSON response from the API if the request is successful.

        Raises
        ------
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
                response.raise_for_status()

    async def get_yields(self, interval: str = "daily"):
        """
        Fetch yield data for various yield maturities from the AlphaVantage API.

        Args
        ----
            interval (str): Specify the interval for the yield data.
            - Must be one of 'daily', 'weekly', or 'monthly'.

        Raises
        ------
            ValueError: Raise error if the provided interval is not one of the allowed values.

        Returns
        -------
            None: Populate the instance variable `yc_data` with the fetched yield data.

        """
        # check if interval is valid for API call
        if interval not in {"daily", "weekly", "monthly"}:
            raise ValueError("Interval value must be one of: 'daily', 'weekly', 'monthly'")

        # retrieve data from API and save to class attribute
        endpoints = get_historical_yield_data_endpoints(interval, self.api_key)
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

    async def get_economic_data(self, interval: str = "daily"):
        """
        Fetch economic data from the AlphaVantage API for CPI, Real GDP per Capita, and Inflation.

        Raises
        ------
            ValueError: Raise error if the provided interval is not one of the allowed values.

        Returns
        -------
            None: Populate the instance variable `economic_data` with the fetched data.

        """
        # check if interval is valid for API call
        if interval not in {"daily", "weekly", "monthly"}:
            raise ValueError("Interval value must be one of: 'daily', 'weekly', 'monthly'")

        # dict of endpoints we will hit for historical data
        endpoints = {
            "CPI": f"function=CPI&interval={interval}&apikey={self.api_key}",
            "RealGDPPerCapita": f"function=REAL_GDP_PER_CAPITA&apikey={self.api_key}",
            "Inflation": f"function=INFLATION&apikey={self.api_key}",
        }

        # retrieve data from API and save to class attribute
        tasks = [self.get_data(endpoint) for endpoint in endpoints.values()]
        responses = await asyncio.gather(*tasks)
        self.economic_data = {
            "CPI": responses[0],
            "RealGDPPerCapita": responses[1],
            "Inflation": responses[2],
        }
