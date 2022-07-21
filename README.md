# Tactical Portfolio Tools
This code repository is ~a collection of tools~ currently just one tool for tactical investing.

# Trade shaping calculator
The app implements the tactical investing advice discribed by [Alfonso Peccatiello](https://twitter.com/MacroAlf) in [this edition](https://themacrocompass.substack.com/p/european-conundrum#details) of his [Macro Compass substack](https://themacrocompass.substack.com/).

> The book targets a 20% annualized return with a 10% maximum peak-to-valley drawdown, and the max loss per trade is defined at 2% of AuM (aggressive, I know: but this strategy represents only a portion of my overall approach to investing my savings). The horizon is 1-3 months.
>
> Trades are sized according to their underlying volatility: a 1.5+ standard deviation move against me (based on 5-yrs rolling monthly history) stops me out, while a trailing profit target strategy is applied if the trade is going my way by moving the next profit target higher and tightening the stop (now making positive P&L) on the way up.
>
> By letting the profits run, I managed to generate a 12% return (6 monthly sigma!) on a single trade this year - the US 2s10s flattener.
>
> A time-based stop is also applied, especially on negative carry trades: if the trade isn't moving in my direction after 3 months, I take it off and re-allocate risk budget.
>
> Trades are structured via futures when available, otherwise options or ETFs.
>
> My win rate is generally around 55% (this year 64%, I am lucky) but as my stops are well defined, the idea is to have my positive P&L trades exceed my negative P&L trades at the end of the year by a decent margin.

So this app will calculate the recommended stop loss, target profit, and size for an investment, all based on what a one standard deviation move is for this investment. I'm calling this app a trade shaping calcuator.

## Functionality

When run, the app will ...
* Ask for a ticker.
* Ask for the dollar value of the tactical portfolio.
* Look up 10 years of monthly returns.
* Calculate the standard deviation.
* Print the recommended stop loss, target profit, and size for the investment.

# Installation

## Dependencies
The only local dependency you need to configure to use this codebase is `docker-compose`. This is great, because once you have docker working, it eliminates the "well it works on my machine" kind of problems. If it works on docker for you, it will work in docker for anyone.

## Install
* Build the image:
  ```console
  docker-compose build
  ```

## Run
* Run the app one time and exit:
  ```console
  docker-compose run --rm app
  ```
* Open a long-running session inside the container:
  ```console
  docker-compose run --rm app bash
  ```
  From here, you can ...
  * Run the trade shaping calculator app.
    ```console
    poetry run python -m trade_shaping_calculator
    ```
  * Run the auto formatter.
    ```console
    poetry run pre-commit run --all-files
    ```
    * For more usage instructions, see [the pre-commit documentation](https://pre-commit.com/).

## Debug
* Documentation [here](https://docs.python.org/3/library/pdb.html).
* Set a breakpoint with `import pdb; pdb.set_trace()`.
  * If you're using vim with [a project-specific .vimrc](https://andrew.stwrt.ca/posts/project-specific-vimrc/), you can type this with `<leader>db`.
* Show where you are with `list`.
* Continue with `continue`.
* Quit with `quit`.

## Add a new python package
This app makes use of [`poetry`](https://python-poetry.org/) to manage packages. See docs there for how to add packages.
