"""
Main application process for the Trading Shaping Calculator.
"""

from calendar import monthrange
from datetime import date

import pandas as pd

# Datareader to download price data from the Yahoo API
import pandas_datareader as web

PORTFOLIO_DRAWDOWN_MAX_PERCENT = 0.02


class TradeShapingCalculator:
    @staticmethod
    def run():
        """
        Given a ticker, looks up the 10y rolling monthly returns of the
        investment. Calculates the 10-year and five-year standard deviations.
        From the latter, calculates a target profit and target profit and stop
        loss exits at 1.5 standard deviations up and down. (The former is just
        for informational purposes.)

        Given a portfolio size, calculates a max allocation so that a one
        standard deviation drawdown would be a 2% loss to the portfolio.

        @return [None]
        """
        ticker = input("Please enter the ticker symbol:\n")

        portfolio_size = input("Please enter the size in dollars of the portfolio:\n")
        portfolio_size = int(portfolio_size)

        # Query one extra month because we will drop it later because it will
        # have a NaN.
        (
            start,
            end,
        ) = TradeShapingCalculator.start_and_end_dates_for_n_monthly_returns(
            10 * 12 + 1
        )
        monthly_prices = TradeShapingCalculator.monthly_prices(ticker, start, end)

        # Drop the first month because it has a NaN
        monthly_percent_changes = monthly_prices.pct_change(periods=1)[1:].rename(
            "monthly percent change"
        )

        ten_year_percent_standard_deviation = monthly_percent_changes.std()
        five_year_percent_standard_deviation = monthly_percent_changes.tail(60).std()
        max_allocation = (
            portfolio_size
            * PORTFOLIO_DRAWDOWN_MAX_PERCENT
            / five_year_percent_standard_deviation
        )
        current_price = web.get_data_yahoo(ticker, date.today())["Adj Close"][0]
        stop_loss = current_price * (1 - (five_year_percent_standard_deviation * 1.5))
        target_profit = current_price * (
            1 + (five_year_percent_standard_deviation * 1.5)
        )

        output = {
            "portfolio_size": portfolio_size,
            "ticker": ticker,
            "current price": current_price,
            "10y percent standard deviation": ten_year_percent_standard_deviation * 100,
            "5y percent standard deviation": five_year_percent_standard_deviation * 100,
            "max allocation": max_allocation,
            "stop loss": stop_loss,
            "stop loss percent": (five_year_percent_standard_deviation * 1.5) * 100,
            "target profit": target_profit,
        }
        output = {k: [v] for k, v in output.items()}
        output = pd.DataFrame(output)

        print()
        print(output.round(2))

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
          is not 200
        @raise [KeyError] If Yahoo can't find the ticker.
        """
        data = web.get_data_yahoo(ticker, start, end)

        # Keep only the adjusted close column
        data = data["Adj Close"]

        # Keep only prices at the last day of each month
        data = data.resample("M").last()

        data = data.rename("monthly prices")

        return data
