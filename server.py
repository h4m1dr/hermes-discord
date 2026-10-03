import os
import threading
import subprocess
import sys
from pathlib import Path
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

def inject_hermes_env():
    """
    Forcefully writes Render environment variables into Hermes' local .env file.
    This prevents Hermes from falling back to default OpenAI settings.
    """
    base_url = os.environ.get("OPENAI_API_BASE")
    api_key = os.environ.get("OPENAI_API_KEY")
    model_name = os.environ.get("OPENAI_MODEL_NAME")

    if not all([base_url, api_key, model_name]):
        print("⚠️ Warning: Missing required OPENAI_* environment variables in Render.")
        return

    # Hermes default configuration directory
    config_dir = Path.home() / ".hermes"
    config_dir.mkdir(parents=True, exist_ok=True)
    env_file = config_dir / ".env"

    # Read existing lines and remove old OPENAI entries to prevent duplicates
    lines = []
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            lines = [
                line for line in f 
                if not line.startswith(("OPENAI_API_BASE=", "OPENAI_API_KEY=", "OPENAI_MODEL_NAME="))
            ]

    # Append the correct, fresh variables from Render
    lines.append(f"OPENAI_API_BASE={base_url}\n")
    lines.append(f"OPENAI_API_KEY={api_key}\n")
    lines.append(f"OPENAI_MODEL_NAME={model_name}\n")

    # Write back to the file
    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Successfully injected LLM config into {env_file}")
    print(f"   Base: {base_url}")
    print(f"   Model: {model_name}")

if __name__ == "__main__":
    # Step A: Inject the correct environment variables before Hermes starts
    inject_hermes_env()

    # Step B: Start the Keep-Alive server in a background daemon thread
    keep_alive_thread = threading.Thread(target=run_keep_alive, daemon=True)
    keep_alive_thread.start()

    # Step C: Start the main Hermes Gateway engine using the official CLI
    print("🚀 Starting Hermes Gateway...")
    try:
        subprocess.run(["hermes", "gateway", "run"], check=True)
    except FileNotFoundError:
        print("❌ Error: 'hermes' command not found. Ensure hermes-agent is installed.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Critical error: Hermes gateway exited with code {e.returncode}")
        sys.exit(1)
