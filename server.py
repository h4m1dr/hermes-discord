import os
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Persistent HTTP server to keep Render port scanner happy (Port 10000)
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
    print("Configuring environment for Hermes Agent...")
    # Force allow all users to prevent unauthorized crashing
    os.environ["GATEWAY_ALLOW_ALL_USERS"] = "true"
    
    # Run hermes gateway in a loop or safe wrapper so if it errors, the web server stays alive
    while True:
        print("Starting Hermes Gateway...")
        try:
            result = subprocess.run(["hermes", "gateway", "run"])
            print(f"Hermes exited with code {result.returncode}, restarting in 5 seconds...")
        except Exception as e:
            print(f"Hermes gateway exception: {e}")
        
        import time
        time.sleep(5)

if __name__ == "__main__":
    # Start the HTTP keep-alive server in a background thread (ensures Render port never dies)
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Start Hermes in the main thread (with safe restart loop)
    run_hermes()
