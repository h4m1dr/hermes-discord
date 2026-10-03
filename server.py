import os
import threading
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Keep-Alive server to satisfy Render's port binding requirement
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Discord Agent is awake and running!")
        
    def log_message(self, format, *args):
        pass  # Disable default HTTP logging to keep console clean

def run_keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    print(f"Keep-alive server running on port {port} to satisfy Render.")
    server.serve_forever()

if __name__ == "__main__":
    # Start the Keep-Alive server in a background daemon thread
    keep_alive_thread = threading.Thread(target=run_keep_alive, daemon=True)
    keep_alive_thread.start()

    # 2. Start the main Hermes Gateway engine
    print("Starting Hermes Gateway...")
    try:
        # Attempt to run the standard Hermes Agent module
        subprocess.run([sys.executable, "-m", "hermes.gateway"], check=True)
    except Exception as e:
        print(f"First method failed: {e}")
        print("Attempting fallback method (hermes gateway run)...")
        try:
            subprocess.run(["hermes", "gateway", "run"], check=True)
        except Exception as e2:
            print(f"Critical error: Cannot start Hermes. {e2}")
            print("Please verify the correct execution command for your bot.")
            sys.exit(1)
