import signal
import sys

from beta_calculator import BetaCalculator


def handle_stop_signals(signum, frame):
    print("\n\nStopping the Beta Calculator...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_stop_signals)
signal.signal(signal.SIGTERM, handle_stop_signals)

print("Starting the Beta Calculator...\n")

BetaCalculator().run()
