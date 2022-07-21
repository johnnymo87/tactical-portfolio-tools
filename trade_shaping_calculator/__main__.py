import signal
import sys

from trade_shaping_calculator import TradeShapingCalculator


def handle_stop_signals(signum, frame):
    print("\n\nStopping the Trade Shaping Calculator...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_stop_signals)
signal.signal(signal.SIGTERM, handle_stop_signals)

print("Starting the Trade Shaping Calculator...\n")

TradeShapingCalculator.run()
