# s400_camera_scheduler

🛠️ **Cradlepoint SDK App for GPIO-Based Camera Power Control on S400 Modems**

## Overview

The `s400_camera_scheduler` is a Cradlepoint SDK application designed to control GPIO pin 1 on S400 modems to manage power to an attached IP camera based on a weekday time schedule. The GPIO pin is activated between **6:00 AM and 5:00 PM**, Monday through Friday. The time is set on the Cradlepoint device which is controlled at the group level based on timezones labeled in the group name. 

## Features

- 🔄 Automatically toggles GPIO pin based on the system time.
- 📆 Operates only on weekdays (Monday through Friday).
- ⏰ Active hours: 6:00 AM to 4:59 PM.
- ⚠️ Logs and corrects mismatched GPIO states.
- 📡 Fully integrated with Cradlepoint's NCOS SDK via `csclient`.

## How It Works

1. **Initialization**:
   - Configures GPIO pin 1 as output.
   - Sets the pin to `HIGH` if it's currently within the scheduled hours.

2. **Scheduler Loop**:
   - Runs every minute.
   - Compares expected vs. actual GPIO state.
   - Corrects state if there's a mismatch.
   - Logs status every cycle.

## Requirements

- Cradlepoint device running NCOS in SDK Dev Mode.
- Pin 1 connected to a camera relay or power switch.
- Python 3.8+ runtime with access to `csclient`.

## Deployment

```bash
# From your development environment
python3 make.py build
python3 make.py install
python3 make.py start
```

## Monitoring

Monitor log output via SDK or system logs:
```bash
python3 make.py status
```

## File Structure

- `s400_camera_scheduler.py`: Main Python script controlling the GPIO logic.
- `package.ini`: Metadata and versioning for SDK packaging.

## License

Proprietary - Blue Line Solutions

## Author

Blue Line Solutions, LLC – Engineering Team