import cp
import time
import datetime

# ------------------------- CONFIG -------------------------
DEFAULT_START_HOUR = 6
DEFAULT_END_HOUR = 17
DEFAULT_DAYS_ACTIVE = [0, 1, 2, 3, 4]  # Weekdays

# -------------------- GPIO Initialization ------------------
cp.put('/control/gpio/CONNECTOR_GPIO_1_CTL', 1)
cp.put('/control/gpio/CONNECTOR_GPIO_SINK_EN', 0)
cp.put('/control/gpio/CONNECTOR_GPIO_1_PH_EN', 1)

# ---------------------- TIME FUNCTIONS ---------------------
def get_router_eastern_time():
    try:
        epoch = cp.get('/status/system/time')
        if not isinstance(epoch, (int, float)):
            cp.log(f"Unexpected time format: {epoch}")
            return None
    except Exception as e:
        cp.log(f"Failed to fetch router time: {e}")
        return None

    utc_time = datetime.datetime.utcfromtimestamp(epoch)
    year = utc_time.year

    # DST starts 2nd Sunday in March
    dst_start = datetime.datetime(year, 3, 8)
    while dst_start.weekday() != 6:
        dst_start += datetime.timedelta(days=1)

    # DST ends 1st Sunday in November
    dst_end = datetime.datetime(year, 11, 1)
    while dst_end.weekday() != 6:
        dst_end += datetime.timedelta(days=1)

    offset = -4 if dst_start <= utc_time < dst_end else -5
    return utc_time + datetime.timedelta(hours=offset)

# ------------------- SCHEDULE LOGIC ------------------------
def should_camera_be_on(now, start_hour, end_hour):
    if now.weekday() not in DEFAULT_DAYS_ACTIVE:
        return False
    
    start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)
    return start_time <= now <= end_time

# ------------------------ MAIN LOOP ------------------------
last_state = None
last_log_minute = -1

time.sleep(30)  # Delay for system stabilization
cp.log("s700gpiocontroller started")

while True:
    now = get_router_eastern_time()
    if not now:
        time.sleep(10)
        continue

    try:
        # Configurable schedule via NetCloud AppData
        start_hour = int(cp.get_appdata('start_hour') or DEFAULT_START_HOUR)
        end_hour = int(cp.get_appdata('end_hour') or DEFAULT_END_HOUR)
        override = cp.get_appdata('manual_override')
        if override == '1':
            state = True
        elif override == '0':
            state = False
        else:
            state = should_camera_be_on(now, start_hour, end_hour)
    except Exception as e:
        cp.log(f"Error reading AppData: {e}")
        state = should_camera_be_on(now, DEFAULT_START_HOUR, DEFAULT_END_HOUR)

    if state != last_state:
        cp.put('/control/gpio/CONNECTOR_GPIO_1', 1 if state else 0)
        cp.put_appdata('gpio1_status', 'ON' if state else 'OFF')
        cp.log(f"GPIO 1 {'ON' if state else 'OFF'} at {now}")
        last_state = state

    # Hourly heartbeat
    if now.minute == 0 and now.minute != last_log_minute:
        cp.log(f"Heartbeat: active at {now}")
        last_log_minute = now.minute

    time.sleep(10)
