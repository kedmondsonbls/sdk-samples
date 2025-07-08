import cp
import time

# Enable GPIO 1 (pin 4) output on S700 for test
cp.put('/control/gpio/USER_GPIO_EN', 1)
cp.put('/control/gpio/CONNECTOR_GPIO_1_CTL', 1)
cp.put('/control/gpio/CONNECTOR_GPIO_SINK_EN', 0)
cp.put('/control/gpio/CONNECTOR_GPIO_1_PH_EN', 1)

cp.log("Starting GPIO 1 cycle test: 2 seconds ON, 2 seconds OFF")

# Manual test script to be run only when started by user
try:
    while True:
        cp.put('/control/gpio/CONNECTOR_GPIO_1', 1)
        cp.log("GPIO 1 ON")
        time.sleep(2)

        cp.put('/control/gpio/CONNECTOR_GPIO_1', 0)
        cp.log("GPIO 1 OFF")
        time.sleep(2)

except KeyboardInterrupt:
    cp.put('/control/gpio/CONNECTOR_GPIO_1', 0)
    cp.log("Test interrupted, GPIO 1 OFF")
