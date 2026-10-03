import os
import threading
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# ۱. سرور Keep-Alive برای راضی نگه داشتن رندر
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Discord Agent is awake and running!")
        
    def log_message(self, format, *args):
        pass # غیرفعال کردن لاگ‌های اضافی HTTP

def run_keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    print(f"✅ Keep-alive server running on port {port} to satisfy Render.")
    server.serve_forever()

if __name__ == "__main__":
    # شروع سرور Keep-Alive در یک ترد جداگانه (پس‌زمینه)
    keep_alive_thread = threading.Thread(target=run_keep_alive, daemon=True)
    keep_alive_thread.start()

    # ۲. استارت زدن موتور اصلی ربات Hermes
    print("🚀 Starting Hermes Gateway...")
    try:
        # تلاش برای اجرای دستور استاندارد Hermes Agent
        subprocess.run([sys.executable, "-m", "hermes.gateway"], check=True)
    except Exception as e:
        print(f"⚠️ روش اول اجرا نشد: {e}")
        print("در حال تلاش برای روش جایگزین (hermes gateway run)...")
        try:
            subprocess.run(["hermes", "gateway", "run"], check=True)
        except Exception as e2:
            print(f"❌ خطای حیاتی: نمی‌توان Hermes را اجرا کرد. {e2}")
            print("لطفاً بررسی کنید که دستور اجرای صحیح ربات شما چیست.")
            sys.exit(1)
