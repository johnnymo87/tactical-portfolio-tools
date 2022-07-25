"""
Main application process for the Momentum Calculator.
"""

from calendar import monthrange
from datetime import date

import pandas as pd

# Datareader to download price data from the Yahoo API
import pandas_datareader as web


class MomentumCalculator:
    @staticmethod
    def one_month():
        """
        Derived from a study written by Volker Flögel, Christian Schlag, and
        Claudia Zunft, called "Momentum-Managed Equity Factors," published in
        the April 2022 issue of the Journal of Banking and Finance.

        This study is summarized here:
        https://alphaarchitect.com/2022/07/momentum-everywhere-including-in-factors/

        Returns two years of momentum signal for a ticker.

        Calculates the 1 month percent change. Z scores it. Uses CDF as an
        activation function, meaning values near zero are bad and values near
        one are good.

        @return [None]
        """
        ticker = input("Please enter the ticker symbol:\n")

        # Query one extra month because we will drop it later because it will
        # have a NaN.
        (
            start,
            end,
        ) = MomentumCalculator.start_and_end_dates_for_n_monthly_returns(10 * 12 + 1)
        monthly_prices = MomentumCalculator.monthly_prices(ticker, start, end)

        # Drop the first month because it has a NaN
        monthly_percent_changes = monthly_prices.pct_change(periods=1)[1:].rename(
            "monthly percent change"
        )

        df = pd.DataFrame(monthly_percent_changes)

        df["5y mean"] = monthly_percent_changes.rolling(60).mean()
        df["5y standard deviation"] = monthly_percent_changes.rolling(60).std()

        def z_score(row):
            return (row["monthly percent change"] - row["5y mean"]) / row[
                "5y standard deviation"
            ]

        df["5y z score"] = df.apply(z_score, axis=1)
        # https://stackoverflow.com/a/54317197/2197402
        df["signal"] = df["5y z score"].rank(pct=True)

        print()
        print(df.tail(24).round(2))

    @staticmethod
    def six_and_12_months():
        """
        Derived from the MSCI algorithm for calculating their momentum index.

        Returns two years of momentum signal for a ticker.

        Calculates the 6 month and 12 month percent change. Adjusts these
        figures for volatility. Z scores them. Combines them. Z scores the
        combined value. Uses CDF as an activation function, meaning values near
        zero are bad and values near one are good.

        @return [None]
        """
        ticker = input("Please enter the ticker symbol:\n")

        # Query 12 extra months because we will drop them later because they
        # will have NaNs.
        (
            start,
            end,
        ) = MomentumCalculator.start_and_end_dates_for_n_monthly_returns((10 + 1) * 12)
        monthly_prices = MomentumCalculator.monthly_prices(ticker, start, end)

        df = pd.DataFrame(monthly_prices)

        df["6 month percent change"] = monthly_prices.pct_change(periods=6)
        df["12 month percent change"] = monthly_prices.pct_change(periods=12)
        df = df[12:]  # Drop the first 12 months because of NaNs

        def adjust_risk(target):
            df[f"5y standard deviation of {target}"] = df[target].expanding().std()

            def _adjust_risk(row):
                return row[target] / row[f"5y standard deviation of {target}"]

            return _adjust_risk

        df["adjusted 6 month momentum"] = df.apply(
            adjust_risk("6 month percent change"), axis=1
        )
        df["adjusted 12 month momentum"] = df.apply(
            adjust_risk("12 month percent change"), axis=1
        )

        def z_score(target):
            df[f"5y standard deviation of {target}"] = df[target].expanding().std()
            df[f"5y mean of {target}"] = df[target].expanding().mean()

            def _z_score(row):
                return (row[target] - row[f"5y mean of {target}"]) / row[
                    f"5y standard deviation of {target}"
                ]

            return _z_score

        df["6 month momentum z score"] = df.apply(
            z_score("adjusted 6 month momentum"), axis=1
        )
        df["12 month momentum z score"] = df.apply(
            z_score("adjusted 12 month momentum"), axis=1
        )

        def combined_score(row):
            return (
                0.5 * row["6 month momentum z score"]
                + 0.5 * row["12 month momentum z score"]
            )

        df["combined momentum"] = df.apply(combined_score, axis=1)
        df["combined momentum z score"] = df.apply(z_score("combined momentum"), axis=1)

        df["signal"] = df["combined momentum z score"].rank(pct=True)

        output_columns = [
            "6 month percent change",
            "12 month percent change",
            "combined momentum z score",
            "signal",
        ]

        print()
        print(df[output_columns].tail(24).round(2))

    @staticmethod
    def start_and_end_dates_for_n_monthly_returns(number_of_months_back):
        """
        Returns a (start, end) date pair that spans n months. The dates are the
        last day of the month of their respective months.

        When we query data with these dates, they will be considered inclusive.

        @param [int] number_of_months_back A positive integer representing how
          many months ago should be the start date.

        @return [datetime.date, datetime.date]
        """
        today = date.today()

        _, end_of_this_month = monthrange(today.year, today.month)
        end_of_this_month = date(today.year, today.month, end_of_this_month)
        if today < end_of_this_month:
            end_date = end_of_this_month + pd.offsets.DateOffset(months=-1)
        elif today == end_of_this_month:
            end_date = end_of_this_month
        else:
            message = (
                "Bug! How can today be greater than the end of this month?! "
                f"(today: {today}, end of this month: {end_of_this_month})"
            )
            raise ValueError(message)

        start_date = end_date + pd.offsets.DateOffset(months=-number_of_months_back)

        return [start_date, end_date]

    @staticmethod
    def monthly_prices(ticker, start, end):
        """
        @param [string] ticker Ticker symbol of the stock
        @param [Date] start Start date of the range (inclusive) of desired data
        @param [Date] end End date of the range (inclusive) of desired data,
          can be `None`

        @return [pandas.core.series.Series]

        @raise [pandas_datareader._utils.RemoteDataError] If Yahoo API response
          is not 200.
        @raise [KeyError] If Yahoo can't find the ticker.
        """
        data = web.get_data_yahoo(ticker, start, end)

        # Keep only the adjusted close column
        data = data["Adj Close"]

        # Keep only prices at the last day of each month
        data = data.resample("M").last()

        data = data.rename("monthly prices")

        return data
