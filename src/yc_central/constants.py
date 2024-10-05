"""Constant variable values used in historical data API class."""

import datetime

TODAY = datetime.datetime.today()
ONE_MONTH_PREV = TODAY - datetime.timedelta(30)
ONE_YEAR_PREV = TODAY - datetime.timedelta(365)

SERIES = {
    "DTB4WK": "4-Week Treasury Bill Secondary Market Rate, Discount Basis",
    "DGS3MO": "Market Yield on U.S. Treasury Securities at 3-Month Constant Maturity, Quoted on an Investment Basis",
    "DGS6MO": "Market Yield on U.S. Treasury Securities at 6-Month Constant Maturity, Quoted on an Investment Basis",
    "DGS1": "Market Yield on U.S. Treasury Securities at 1-Year Constant Maturity, Quoted on an Investment Basis",
    "DGS2": "Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity, Quoted on an Investment Basis",
    "DGS5": "Market Yield on U.S. Treasury Securities at 5-Year Constant Maturity, Quoted on an Investment Basis",
    "DGS7": "Market Yield on U.S. Treasury Securities at 7-Year Constant Maturity, Quoted on an Investment Basis",
    "DGS10": "Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis",
    "DGS30": "Market Yield on U.S. Treasury Securities at 30-Year Constant Maturity, Quoted on an Investment Basis",
    "T10Y3M": "10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity",
    "T10Y2Y": "10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity",
    "SP500": "S&P 500",
    "VIXCLS": "CBOE Volatility Index: VIX",
}
