import time
import datetime
from csclient import EventingCSClient

cp = EventingCSClient('s400_camera_scheduler')
PIN = 1

def is_weekday():
    return datetime.datetime.now().weekday() < 5  # Monday=0, Friday=4

def is_active_time():
    now = datetime.datetime.now()
    return 6 <= now.hour < 17  # 6:00 AM to 4:59 PM

def set_gpio(state: bool):
    response = cp.put(f"/config/system/gpio_actions/pin/{PIN}/enabled", state)
    cp.log(f"GPIO {PIN} set to {'HIGH' if state else 'LOW'} | Response: {response}")

def get_gpio_state():
    try:
        return cp.get(f"/status/gpio_actions/pin/{PIN}/enabled")
    except Exception as e:
        cp.log(f"⚠️ Failed to read GPIO state: {e}")
        return None

def initialize_gpio():
    cp.log(f"Initializing GPIO pin {PIN}")
    cp.put(f"/config/system/gpio_actions/pin/{PIN}/direction", "out")
    cp.put(f"/config/system/gpio_actions/pin/{PIN}/io_type", "lvttl")
    cp.put(f"/config/system/gpio_actions/pin/{PIN}/level", "high")

    # Apply correct initial state
    active = is_weekday() and is_active_time()
    set_gpio(active)

def run_scheduler():
    cp.log("🟢 GPIO weekday scheduler started...")
    while True:
        now = datetime.datetime.now()
        expected_state = is_weekday() and is_active_time()
        actual_state = get_gpio_state()

        cp.log(f"🕒 {now.strftime('%Y-%m-%d %H:%M:%S')} | Expected: {'HIGH' if expected_state else 'LOW'} | Actual: {'HIGH' if actual_state else 'LOW'}")

        if actual_state != expected_state:
            cp.log("⚠️ GPIO state mismatch. Correcting...")
            set_gpio(expected_state)

        time.sleep(60)

if __name__ == "__main__":
    try:
        cp.log("🔧 s400_camera_scheduler initializing...")
        initialize_gpio()
        run_scheduler()
    except Exception as e:
        cp.log(f"❌ Fatal error in scheduler: {e}")
