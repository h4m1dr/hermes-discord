import os
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Simple HTTP request handler to keep Render's port scanner happy
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Discord Bot is active and running!")

def run_server():
    # Fetch port from environment variable assigned by Render, default to 10000
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    print(f"Keep-alive web server running on port {port}...")
    server.serve_forever()

def run_hermes():
    print("Starting Hermes Gateway for Discord...")
    # Execute the official hermes gateway command for Discord channel
    subprocess.run(["hermes", "gateway", "--channel", "discord"])

if __name__ == "__main__":
    # Start the web server in a background thread to prevent Render port timeout
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Start the main Hermes Discord bot process
    run_hermes()
