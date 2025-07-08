
# s700gpiocontroller

A Cradlepoint NCOS SDK application to control GPIO 1 (pin 4) output power to a connected device (e.g., camera) based on a configurable weekday schedule. Designed to run on S700-series routers in DEV mode.

---

## 📦 Application Overview

This application:
- Controls GPIO 1 to power a device during configured weekday hours (e.g., 6:00 AM to 5:00 PM, Mon–Fri).
- Logs GPIO events and heartbeat messages.
- Uses Eastern Time with Daylight Saving Time handling.
- Can be overridden via NetCloud **AppData**.
- Automatically restarts after reboot if `auto_start`, `restart`, and `reboot` are enabled.

---

## 🛠 Files & Structure

| File                   | Purpose                                                                 |
|------------------------|-------------------------------------------------------------------------|
| `s700gpiocontroller.py` | Main application logic (GPIO control and scheduling)                   |
| `cp.py`                | SDK communication module (from Cradlepoint SDK)                         |
| `package.ini`          | App metadata and settings                                               |
| `sdk_settings.ini`     | Developer environment settings (target IP, login, app name, etc.)       |
| `start.sh`             | Startup script to invoke the controller                                 |
| `make.py`              | Build/Deploy tool for packaging, installing, starting, stopping the app |
| `s700gpiocontroller.tar.gz` | Packaged version of the app, ready to install on router             |

---

## ⏱️ Scheduling Logic

- **Defaults:**
  - Start: 6:00 AM
  - End: 5:00 PM
  - Days Active: Monday to Friday
- **Time Zone**: Eastern Time (auto-adjusts for DST)
- **Overrides via AppData:**
  - `manual_override=1` → Forces GPIO ON
  - `manual_override=0` → Forces GPIO OFF
  - `start_hour` / `end_hour` → Override active period

---

## 🚦GPIO Behavior

| State         | GPIO Action                     |
|---------------|----------------------------------|
| Active hours  | Sets `/control/gpio/CONNECTOR_GPIO_1` to 1 (ON) |
| Outside hours | Sets `/control/gpio/CONNECTOR_GPIO_1` to 0 (OFF) |
| Logs state    | `gpio1_status` → `ON` or `OFF` in AppData        |

---

## 🧪 Logging

- Logs initialization, changes in GPIO state, and hourly heartbeat messages via `cp.log()`.
- Example:
  ```
  GPIO 1 ON at 2025-07-06 06:00:00
  Heartbeat: active at 2025-07-06 08:00:00
  ```

---

## 🔧 Setup & Deployment

### 1. Configure Environment

Edit `sdk_settings.ini` with:
```ini
[sdk]
app_name=s700gpiocontroller
dev_client_ip=10.1.132.1
dev_client_username=bls
dev_client_password=your_password_here
```

### 2. Build the App
```bash
python3 make.py package
```

### 3. Install to Router
```bash
python3 make.py install
```

### 4. Start the App
```bash
python3 make.py start
```

### 5. (Optional) Auto-start on reboot

Ensure the following are set in `package.ini`:
```ini
auto_start = true
restart = true
reboot = true
```

---

## 🧼 Cleanup
To remove build artifacts:
```bash
python3 make.py clean
```

To uninstall the app:
```bash
python3 make.py uninstall
```

To purge all SDK apps:
```bash
python3 make.py purge
```

---

## 🧪 Testing & Logs

You can monitor logs via the router's CLI or NetCloud.

To force a manual test:
- Set `manual_override=1` in AppData to force GPIO ON
- Set `manual_override=0` to force GPIO OFF
- Remove `manual_override` to resume schedule control

---

## 🔐 Security Note

Passwords in `sdk_settings.ini` are stored in plain text. Ensure file access is restricted.

---

## 👨‍💻 Credits

Created by Blue Line Solutions using the Cradlepoint NCOS SDK.
