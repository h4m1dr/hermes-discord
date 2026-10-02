import os
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

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
    print("Starting Hermes Gateway for Discord...")
    # اجرای دستور رسمی گیت‌وی هرمس برای دیسکورد
    subprocess.run(["hermes", "gateway", "--channel", "discord"])

if __name__ == "__main__":
    # اجرای وب‌سرور در پس‌زمینه برای اینکه Render پورت باز ببیند و تایم‌اوت ندهد
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # اجرای ترد اصلی بات دیسکورد هرمس
    run_hermes()
