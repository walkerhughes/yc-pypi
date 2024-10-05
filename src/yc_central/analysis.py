"""Utils functions to perform analysis of US Treasury Yield Curve."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from yc_central.historical import HistoricalFredDataAPI


class DataAnalysis(HistoricalFredDataAPI):
    """
    DataAnalysis class for performing analytical investigations on US Treasury Yield Curve data.

    Inherits from HistoricalFredDataAPI to utilize data retrieval methods.

    """

    def calculate_yield_curve_inversion(
        self,
        short_term: str = "DGS2",
        long_term: str = "DGS10",
    ) -> pd.DataFrame:
        """
        Calculate yield curve inversion based on the difference between long-term and short-term yields.

        Args
        ----
            :short_term str: Series ID for short-term yield (e.g., "DGS2").
            :long_term str: Series ID for long-term yield (e.g., "DGS10").

        Returns
        -------
            :pd.DataFrame: DataFrame with an additional column indicating inversion (1) or normal (0).

        """
        data = self.get_all_yield_series()
        inversion_diff = data[long_term] - data[short_term]
        data["Yield_Curve_Inversion"] = np.where(inversion_diff < 0, 1, 0)
        return data[["Date", "Yield_Curve_Inversion"]]

    def calculate_contango_ratio(
        self,
        near_term: str = "DGS3MO",
        far_term: str = "DGS10",
    ) -> pd.DataFrame:
        """
        Calculate contango ratio based on the difference between far-term and near-term yields.

        Args
        ----
            :near_term str: Series ID for near-term yield (e.g., "DGS3MO").
            :far_term str: Series ID for far-term yield (e.g., "DGS10").

        Returns
        -------
            :pd.DataFrame: DataFrame with contango ratio.

        """
        data = self.get_all_yield_series()
        contango_diff = data[far_term] - data[near_term]
        data["Contango_Ratio"] = contango_diff / data[near_term]
        return data[["Date", "Contango_Ratio"]]

    def rolling_regression_coefficients(
        self,
        dependent_var: str,
        independent_var: str,
        window: int = 60,
    ) -> pd.DataFrame:
        """
        Perform rolling window regression and return rolling coefficients.

        Args
        ----
            :dependent_var str: Series ID for the dependent variable.
            :independent_var str: Series ID for the independent variable.
            :window int: Rolling window size.

        Returns
        -------
            :pd.DataFrame: DataFrame with rolling slope and intercept coefficients.

        """
        data = self.get_all_yield_series()
        df = data[[dependent_var, independent_var]].dropna().reset_index(drop=True)

        slopes = []
        intercepts = []
        for i in range(len(df) - window + 1):
            window_data = df.iloc[i : i + window]
            X = window_data[independent_var].values.reshape(-1, 1)
            y = window_data[dependent_var].values
            model = LinearRegression()
            model.fit(X, y)
            slopes.append(model.coef_[0])
            intercepts.append(model.intercept_)

        rolling_dates = data["Date"].dropna().reset_index(drop=True)[window - 1 :]
        regression_df = pd.DataFrame(
            {
                "Date": rolling_dates,
                "Slope": slopes,
                "Intercept": intercepts,
            }
        )
        return regression_df

    def calculate_rolling_volatility(
        self,
        series_id: str,
        window: int = 30,
    ) -> pd.DataFrame:
        """
        Calculate rolling volatility (standard deviation) for a specified series.

        Args
        ----
            :series_id str: Series ID to calculate volatility for.
            :window int: Rolling window size.

        Returns
        -------
            :pd.DataFrame: DataFrame with rolling volatility.

        """
        data = self.get_single_series(fred_series_name=series_id)
        data["Rolling_Volatility"] = data[series_id].rolling(window=window).std()
        return data[["Date", "Rolling_Volatility"]]

    def calculate_rolling_correlation(
        self,
        series_id_1: str,
        series_id_2: str,
        window: int = 60,
    ) -> pd.DataFrame:
        """
        Calculate rolling correlation between two specified series.

        Args
        ----
            :series_id_1 str: First series ID.
            :series_id_2 str: Second series ID.
            :window int: Rolling window size.

        Returns
        -------
            :pd.DataFrame: DataFrame with rolling correlation.

        """
        data = self.get_all_yield_series()
        data["Rolling_Correlation"] = data[series_id_1].rolling(window=window).corr(data[series_id_2])
        return data[["Date", "Rolling_Correlation"]]
