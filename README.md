# Tactical Portfolio Tools
This code repository is ~a collection of tools~ currently just one tool for tactical investing.

# Beta calculator
The app implements the tactical investing advice discribed by [Alfonso Peccatiello](https://twitter.com/MacroAlf) in [this edition](https://themacrocompass.substack.com/i/37808996/the-tactical-approach) of his [Macro Compass substack](https://themacrocompass.substack.com/).

> The rules of the game are the following.
>
> 1. I invest long/short in global macro products with **10% of my savings**. The bulk of my savings is invested in a long-term structural portfolio (more on that later).
>
> 2. Let's call this 10% = 10.000 EUR as a starting amount.
>
> 3. The objective is to **make >10% total return** on this portfolio. At the end of the year, we will compare the return generated/risk taken versus the benchmark long-term structural allocation. Disclaimer: that b***h is hard to beat!
>
> 4. Every trade has a **skewed stop/initial profit target**: hard stop at -2.5% of remaining capital and initial profit target >2.5% (generally 1.5x or more). This way **I can be right <50%** of the times and still make money at year-end if I am thoroughly disciplined in hitting my stops.
>
> 5. The time horizon for trades is generally **1+ months**.
>
> 6. In order not to hit stops too often, I place them at **1 standard deviation** distance from today's entry price calculated using **10y rolling monthly returns** and assuming a normal distribution. The entry size is adjusted such that I can lose max 2.5% of my capital if that 1-sigma move hits me.
>
> 7. I will always **cut my losses and let my profits run**. The former is easy to understand. The latter means that if I hit my first profit target, I move it up by a bit and move up my new stop loss (now a profit target) by a bit. Profits keep on running until I hit my new stop (now a profit).
>
> Yes I know, it's not nearly a perfectly scientific approach and I am simplifying many things, but it should work as a general framework to try and see how my calls are doing.

So this app will calculate the recommended stop loss, target profit, and size for an investment. This is all based on what a one standard deviation move is, which related to the concept of [beta](https://www.investopedia.com/terms/b/beta.asp), so I'm calling this app a beta calcuator for the lack of a better name.

## Functionality

When run, the app will ...
* Ask for a ticker.
* Ask for the dollar value of the tactical portfolio.
* Look up 10 years of monthly returns.
* Calculate the standard deviation.
* Print the recommended stop loss, target profit, and size for the investment.

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
  * Run the beta calculator app.
    ```console
    poetry run python -m beta_calculator
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
