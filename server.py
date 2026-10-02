import os
import threading
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Simple HTTP server to keep Render port scanner happy and prevent timeouts
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Proxy Wake-up Bot is active and running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    print(f"Keep-alive web server running on port {port}...")
    server.serve_forever()

# 2. Background task to periodically ping the main Hermes Render URL to keep it awake if needed
def background_pinger():
    target_url = os.environ.get("MAIN_HERMES_URL", "https://your-main-hermes-app.onrender.com")
    while True:
        try:
            # Send a light ping to wake up the main service
            response = requests.get(target_url, timeout=10)
            print(f"Pinged main Hermes service, status: {response.status_code}")
        except Exception as e:
            print(f"Wake-up ping failed: {e}")
        
        # Ping every 10 minutes to prevent sleep
        time.sleep(600)

if __name__ == "__main__":
    # Start the web server in a background thread to satisfy Render port binding
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Optional: Start the pinger thread if automatic background waking is desired
    pinger_thread = threading.Thread(target=background_pinger, daemon=True)
    pinger_thread.start()

    # Keep the main process alive
    print("Proxy manager started successfully.")
    while True:
        time.sleep(1)
