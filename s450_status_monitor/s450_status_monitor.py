from csclient import EventingCSClient
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

cp = EventingCSClient("s450_status_monitor")

PORT = 8182
WEB_MESSAGE = "Hello from http_test_server"
VERSION = "1.1.0"

cp.log(f"✅ Starting HTTP server on port {PORT}")
cp.log("✅ Serving routes: /status, /health, /version")

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        cp.log(f"📥 Received GET request: {self.path}")
        if self.path == "/status":
            self._respond_json(self._get_status())
        elif self.path == "/health":
            self._respond_text("OK")
        elif self.path == "/version":
            self._respond_text(f"s450_status_monitor v{VERSION}")
        else:
            self.send_response(404)
            self.end_headers()

    def _get_status(self):
        try:
            temp = cp.get("/status/system/temperature")
            voltage = cp.get("/status/power_usage/voltage")
            camera_power = cp.get("/config/system/gpio_actions/pin/1/enabled")

            return {
                "temperature": temp,
                "voltage": voltage,
                "camera_power": camera_power,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            cp.log(f"❌ Error in _get_status: {e}")
            return {"error": str(e)}

    def _respond_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _respond_text(self, text):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))

    def log_message(self, format, *args):
        return  # suppress default logging

# Start HTTP server
try:
    server = HTTPServer(("0.0.0.0", PORT), StatusHandler)
    cp.log("🚀 s450_status_monitor is running.")
    cp.log("📡 Routes available: /status, /health, /version")
    server.serve_forever()
except Exception as e:
    cp.log(f"🔥 Server failed: {e}")
