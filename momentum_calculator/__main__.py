import signal
import sys

from momentum_calculator import MomentumCalculator


def handle_stop_signals(signum, frame):
    print("\n\nStopping the Momentum Calculator...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_stop_signals)
signal.signal(signal.SIGTERM, handle_stop_signals)

print("Starting the Momentum Calculator...\n")

prompt = "\n".join(
    ("Please select a calculator:", "1. One month", "2. Six and 12 months", "")
)
choice = input(prompt)
if int(choice) == 1:
    MomentumCalculator.one_month()
elif int(choice) == 2:
    MomentumCalculator.six_and_12_months()
else:
    raise ValueError(f"Invalid choice: {choice}")
