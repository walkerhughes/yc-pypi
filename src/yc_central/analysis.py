"""Utils functions to perform analysis of US Treasury Yield Curve."""

import asyncio

import numpy as np
import pandas as pd

from yc_central.historical import HistoricalDataAPI


def get_inversion_status(api_key: str = ""):
    async def async_get_inversion_status():
        api = HistoricalDataAPI(api_key=api_key)
        await api.get_yields()
        return api.yc_data

    # Run the asynchronous function and return its result synchronously
    return asyncio.run(async_get_inversion_status())
