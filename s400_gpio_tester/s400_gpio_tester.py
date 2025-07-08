import time
import logging
from csclient import EventingCSClient

client = EventingCSClient('gpio2_controller')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gpio2_controller")

PINS = [0, 1]
INTERVAL = 2  # seconds

def initialize_gpio():
    for pin in PINS:
        logger.info(f"Configuring GPIO pin {pin}")
        client.put(f"/config/system/gpio_actions/pin/{pin}/direction", "out")
        client.put(f"/config/system/gpio_actions/pin/{pin}/io_type", "lvttl")
        client.put(f"/config/system/gpio_actions/pin/{pin}/level", "high")
        client.put(f"/config/system/gpio_actions/pin/{pin}/enabled", True)
    time.sleep(0.2)

def toggle_gpio(state: bool):
    for pin in PINS:
        client.put(f"/config/system/gpio_actions/pin/{pin}/enabled", state)
    logger.info(f"GPIO {PINS[0]} & {PINS[1]} set {'HIGH' if state else 'LOW'}")

def cycle_gpio():
    logger.info("Starting GPIO 1 & 2 cycle using 'enabled' toggle...")
    while True:
        toggle_gpio(False)
        time.sleep(INTERVAL)
        toggle_gpio(True)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    initialize_gpio()
    cycle_gpio()
