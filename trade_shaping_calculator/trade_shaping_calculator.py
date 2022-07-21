"""
Main application process for the Trading Shaping Calculator.
"""

from calendar import monthrange
from datetime import date

import pandas as pd

# Datareader to download price data from the Yahoo API
import pandas_datareader as web

PORTFOLIO_DRAWDOWN_MAX_PERCENT = 0.025


class TradeShapingCalculator:
    @staticmethod
    def run():
        """
        Given a ticker, looks up the 10y rolling monthly returns of the
        investment. From this, calculates a stop loss and target profit that
        are one and 1.5 standard deviations respectively.

        Given a portfolio size, calculates a max allocation so that a one
        standard deviation drawdown would be a 2.5% loss to the portfolio.

        @return [None]
        """
        ticker = input("Please enter the ticker symbol:\n")

        portfolio_size = input("Please enter the size in dollars of the portfolio:\n")
        portfolio_size = int(portfolio_size)

        ticker_percent_monthly_changes = TradeShapingCalculator.percent_monthly_changes(
            ticker
        )
        ticker_percent_standard_deviation = ticker_percent_monthly_changes.std()
        max_allocation = (
            portfolio_size
            * PORTFOLIO_DRAWDOWN_MAX_PERCENT
            / ticker_percent_standard_deviation
        )
        current_price = web.get_data_yahoo(ticker, date.today())["Adj Close"][0]
        stop_loss = current_price * (1 - ticker_percent_standard_deviation)
        target_profit = current_price * (1 + (ticker_percent_standard_deviation * 1.5))

        output = {
            "portfolio_size": portfolio_size,
            "ticker": ticker,
            "current price": current_price,
            "percent standard deviation": ticker_percent_standard_deviation * 100,
            "max allocation": max_allocation,
            "stop loss": stop_loss,
            "target profit": target_profit,
        }
        output = {k: [v] for k, v in output.items()}
        output = pd.DataFrame(output)

        print()
        print(output.round(2))

    @staticmethod
    def start_and_end_dates_for_10y_of_monthly_returns():
        """
        Returns a (start, end) date pair that spans 10 years. The dates are the
        last day of the month of their respective months.

        When we query data with these dates, they will be considered inclusive.

        @return [Date, Date]
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

        # Offset start date from end date by 10 years and one month. The one
        # month so we can use it calculate the percent change that occured
        # in month one of 10 years ago.
        start_date = end_date + pd.offsets.DateOffset(years=-10, months=-1)

        return [start_date, end_date]

    @staticmethod
    def percent_monthly_changes(ticker):
        """
        @param [string] ticker Ticker symbol of the stock
        @param [Date] start Start date of the range (inclusive) of desired data
        @param [Date] end End date of the range (inclusive) of desired data,
          can be `None`

        @return [pandas.core.frame.DataFrame]
        @return [pandas.core.series.Series]

        @raise [pandas_datareader._utils.RemoteDataError] If Yahoo API response
          is not 200
        """
        (
            start,
            end,
        ) = TradeShapingCalculator.start_and_end_dates_for_10y_of_monthly_returns()

        data = web.get_data_yahoo(ticker, start, end)

        # Keep only the adjusted close column
        data = data["Adj Close"]

        # Keep only prices at the last day of each month
        data = data.resample("M").last()

        # Calculate the percent change
        data = data.pct_change()[1:]

        return data
