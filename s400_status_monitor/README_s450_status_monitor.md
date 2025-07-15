# s450_status_monitor

**Version:** 1.1.0  
**Vendor:** BlueLine  
**Platform:** Cradlepoint S450 (NCOS SDK)  
**Author:** Kevin Edmondson  
**Port:** `8182`

---

## 🧭 Overview

`s450_status_monitor` is a Cradlepoint NCOS SDK application that launches a lightweight HTTP server for external monitoring tools such as **PRTG**. It provides real-time status data from the router's system sensors and GPIO configuration via simple RESTful routes.

---

## 🌐 HTTP Endpoints

| Endpoint       | Method | Description                                      |
|----------------|--------|--------------------------------------------------|
| `/status`      | GET    | Returns system temperature, input voltage, and GPIO 1 camera power state in JSON |
| `/health`      | GET    | Basic health check – always returns `OK`         |
| `/version`     | GET    | Returns version string of the app                |

---

## 🔌 Example Output

`GET /status`

```json
{
  "temperature": 34,
  "voltage": 12.2668,
  "camera_power": true,
  "timestamp": "2025-07-14 09:08:02"
}
```

---

## ⚙️ Monitored System Values

- **Temperature:** Pulled from `/status/system/temperature`
- **Voltage:** Pulled from `/status/power_usage/voltage`
- **GPIO Camera Power:** Reads whether GPIO pin 1 is currently enabled
- **Timestamp:** Current system time when status is served

---

## 🚀 Deployment Instructions

1. **Clean and rebuild the SDK**  
   ```bash
   python3 make.py clean
   python3 make.py uuid
   python3 make.py build
   ```

2. **Install and start the app**  
   ```bash
   python3 make.py install
   python3 make.py start
   ```

3. **Verify it's running**  
   ```bash
   python3 make.py status
   ```

4. **Test the server (from another host)**  
   ```bash
   curl http://<router-ip>:8182/status
   ```

---

## 🛑 Error Handling

- Failures in data retrieval from the Cradlepoint system are caught and logged
- A JSON error message will be returned in `/status` if something fails internally

---

## 📁 File Structure

```text
s450_status_monitor/
├── __init__.py          # Main SDK logic and HTTP server
├── package.ini          # Metadata and config
```

---

## 📓 Notes

- This service is ideal for PRTG or any external monitoring service that supports JSON or HTTP health checks.
- You can change the port by editing the `PORT` variable in `__init__.py`.

---

## 🧪 Future Enhancements

- Add uptime tracking
- Include GPIO input (e.g., solar panel voltage check)
- PRTG XML format option for native parsing

---