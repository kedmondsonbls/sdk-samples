# GPIO 2-Second Cycle Test

This Cradlepoint NCOS SDK application (`gpio2secondcycletest`) is a diagnostic tool for manually cycling GPIO 1 on the S700 series modems. It toggles the GPIO pin ON and OFF every 2 seconds in an infinite loop until interrupted. This is useful for testing connected hardware such as relays or cameras.

---

## Features

- Cycles GPIO 1 (pin 4) ON for 2 seconds, OFF for 2 seconds.
- Sends status logs to NetCloud for visibility.
- Designed for manual execution only (not set to auto-start).
- Includes graceful shutdown on keyboard interrupt.

---

## Files

- `gpio2secondcycletest.py` – Main application logic.
- `start.sh` – Shell script for running the application via SDK.
- `package.ini` – Metadata for the application including UUID, versioning, and execution behavior.
- `sdk_settings.ini` – Stores connection parameters and app configuration.
- `cp.py` – Interface to the Cradlepoint device API.
- `make.py` – SDK utility for packaging, deploying, and managing NCOS apps.

---

## Installation and Execution

### 1. Update `sdk_settings.ini`

Ensure the file contains the correct values:

```ini
[sdk]
app_name=gpio2secondcycletest
dev_client_ip=<DEVICE_IP>
dev_client_username=<USERNAME>
dev_client_password=<PASSWORD>
```

### 2. Package the App

```bash
python3 make.py package
```

### 3. Install the App on the Device

```bash
python3 make.py install
```

### 4. Start the App

```bash
python3 make.py start
```

You should now see the GPIO cycling ON/OFF every 2 seconds and logs in NetCloud.

---

## Stopping the App

To stop the app:

```bash
python3 make.py stop
```

To uninstall:

```bash
python3 make.py uninstall
```

---

## Notes

- **auto_start** is set to `false`, meaning it won’t run after a reboot.
- This app is intended for manual testing or verification workflows.
- Compatible with firmware `7.25+` on Cradlepoint S700 series devices.

---

## License

Property of **BlueLineSolutions**. For internal diagnostic and validation use only.