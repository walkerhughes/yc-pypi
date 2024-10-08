"""Utils functions to perform analysis of US Treasury Yield Curve."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def calculate_yield_inversion(
    df: pd.DataFrame,
    short_term: str = "DGS2",
    long_term: str = "DGS10",
) -> pd.DataFrame:
    """
    Calculate yield curve inversion based on the difference between long-term and short-term yields.

    Args
    ----
        data_api (HistoricalFredDataAPI): Instance to retrieve yield data.
        short_term (str): Series ID for short-term yield (e.g., "DGS2").
        long_term (str): Series ID for long-term yield (e.g., "DGS10").

    Returns
    -------
        pd.DataFrame: DataFrame with Date and Yield_Curve_Inversion columns.

    """
    inversion_diff = df[long_term] - df[short_term]
    return pd.DataFrame(
        {
            "Date": df["Date"].values,
            f"{long_term}-{short_term}_Spread": inversion_diff,
            f"{long_term}-{short_term}_Inversion": np.where(inversion_diff < 0, 1, 0),
        }
    )


def rolling_regression_coefficients(
    df: pd.DataFrame,
    dependent_var: str,
    independent_var: str,
    window: int = 2,
) -> pd.DataFrame:
    """
    Perform rolling window regression and return rolling coefficients.

    Args
    ----
        df (pd.DataFrame): Dataframe of historical data.
        dependent_var (str): Series ID for the dependent variable.
        independent_var (str): Series ID for the independent variable.
        window (int): Rolling window size.

    Returns
    -------
        pd.DataFrame: DataFrame with Date, Slope, and Intercept columns.

    """
    df = df[[dependent_var, independent_var]].ffill().reset_index(drop=True).dropna()
    slopes = []
    intercepts = []
    window = 14

    for i in range(len(df) - window + 1):
        window_data = df.iloc[i : i + window]
        X = window_data[independent_var].values.reshape(-1, 1)
        y = window_data[dependent_var].values
        model = LinearRegression()
        model.fit(X, y)
        slopes.append(model.coef_[0])
        intercepts.append(model.intercept_)

    rolling_dates = df["Date"].dropna().reset_index(drop=True)[window - 1 :]

    regression_df = pd.DataFrame(
        {
            "Date": rolling_dates,
            "Slope": slopes,
            "Intercept": intercepts,
        }
    )
    return regression_df


def calculate_rolling_correlation(
    df: pd.DataFrame,
    series_id_1: str,
    series_id_2: str,
    window: int = 60,
) -> pd.DataFrame:
    """
    Calculate rolling correlation between two specified series.

    Args
    ----
        df (pd.DataFrame): Dataframe of historical data to analyze.
        series_id_1 (str): First series ID.
        series_id_2 (str): Second series ID.
        window (int): Rolling window size.

    Returns
    -------
        pd.DataFrame: DataFrame with Date and Rolling_Correlation columns.

    """
    rolling_corr = df[series_id_1].rolling(window=window).corr(df[series_id_2])
    return pd.DataFrame({"Date": df["Date"].values, f"{series_id_1}_{series_id_2}_Rolling_Correlation": rolling_corr})
