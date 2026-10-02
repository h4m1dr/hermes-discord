import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

# پورت رندر
PORT = int(os.environ.get("PORT", 10000))
MAIN_APP_URL = os.environ.get("MAIN_APP_URL", "https://hermes-discord.onrender.com")

class WakeUpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # بررسی اینکه آیا درخواست بیدارباش است یا پینگ معمولی رندر
        if self.path == "/wake":
            try:
                # پینگ کردن سرور اصلی برای بیدار کردن آن از حالت Sleep
                req = urllib.request.Request(MAIN_APP_URL)
                with urllib.request.urlopen(req, timeout=5) as response:
                    status = response.getcode()
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Wake-up signal sent to main app. Status: {status}".encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Failed to wake up main app: {str(e)}".encode())
        else:
            # پاسخ استاندارد برای راضی نگه داشتن پورت اسکنر Render
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Proxy Wake-Up Bot is active and running!")

def run_server():
    server = HTTPServer(('0.0.0.0', PORT), WakeUpHandler)
    print(f"Wake-up proxy server running on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    # اجرای سرور در پورت اصلی رندر
    run_server()
