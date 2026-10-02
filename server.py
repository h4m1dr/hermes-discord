import os
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. HTTP server to keep Render port scanner happy (Port 10000)
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Discord Bot is active and running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    print(f"Keep-alive web server running on port {port}...")
    server.serve_forever()

def run_hermes():
    print("Configuring and starting Hermes Agent for Discord...")
    
    # Optional: If hermes needs environment variables explicitly exported for python runtime
    os.environ["GATEWAY_ALLOW_ALL_USERS"] = "true"
    
    # Run hermes gateway using the stable interactive/run command
    # Hermes reads DISCORD_BOT_TOKEN and LLM keys directly from os.environ
    try:
        subprocess.run(["hermes", "gateway", "run"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hermes gateway exited with error: {e}")

if __name__ == "__main__":
    # Start the HTTP keep-alive server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Start Hermes gateway in the main thread
    run_hermes()
