"""API class to fetch yield curve data from AlphaVantage endpoints."""

import datetime
from functools import reduce

import pandas as pd
from fredapi import Fred

from yc_central.constants import (
    ONE_MONTH_PREV,
    SERIES,
    TODAY,
)


class HistoricalFredDataAPI:
    """
    Wrapper class around FRED API to retrieve historical data on US Treasuty Yield Curve.

    Args:
    ----
    :fred_api_key str: API key for FRED API.

    """

    def __init__(self, fred_api_key):
        self.api_key = fred_api_key
        self.fred = Fred(api_key=fred_api_key)

    def get_single_series(
        self,
        fred_series_name: str = "SP500",
        observation_start: datetime.datetime = ONE_MONTH_PREV,
        observation_end: datetime.datetime = TODAY,
        frequency: str = "d",
    ) -> pd.DataFrame:
        """
        Retrieve a data series from FRED API for analysis.

        Args
        ----
            :fred_series_name str: Name of data series to retrieve.
            :observation_start datetime.datetime: Start date of data retrieval.
            :observation_end datetime.datetime: End date of data retrieval.
            :frequency str: Frequency to retrieve data (daily, weekly, monthly).

        Returns
        -------
            :pd.DataFrame: Pandas DataFrame object of historical data.

        """
        if frequency not in {"d", "w", "bw", "m", "q", "sa", "a"}:
            raise ValueError('Interval value must be one of: "d", "w", "bw", "m", "q", "sa", "a"')
        try:
            # fetch historical data series from FRED
            data = self.fred.get_series(
                series_id=fred_series_name,
                observation_start=observation_start,
                observation_end=observation_end,
                frequency=frequency,
            )
            # return data in pd.DataFrame object instead of pd.Series
            return pd.DataFrame({"Date": data.index, fred_series_name: data.values})
        # raise error if a series is unavailable
        except Exception as e:
            raise ValueError(f"Could not retrieve series {fred_series_name}.\n\n{e}")

    def get_all_yield_series(
        self,
        observation_start: datetime.datetime = ONE_MONTH_PREV,
        observation_end: datetime.datetime = TODAY,
        frequency: str = "d",
    ) -> pd.DataFrame:
        """
        Retrieve data series from constants.SERIES from FRED API for analysis.

        Args
        ----
            :observation_start datetime.datetime: Start date of data retrieval.
            :observation_end datetime.datetime: End date of data retrieval.
            :frequency str: Frequency to retrieve data (daily, weekly, monthly).

        Returns
        -------
            :pd.DataFrame: Pandas DataFrame object of historical data series joined together.

        """
        # retrieve data for series in yc_central.constants.SERIES
        dfs = []
        for series_name in SERIES:
            dfs.append(
                self.get_single_series(
                    fred_series_name=series_name,
                    observation_start=observation_start,
                    observation_end=observation_end,
                    frequency=frequency,
                )
            )
        # merge the individual dataframes together and return
        merged_dfs = reduce(lambda left, right: pd.merge(left, right, on="Date", how="left"), dfs)
        return merged_dfs
