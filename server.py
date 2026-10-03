import os
import threading
import subprocess
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Discord Agent is awake and running!")
        
    def log_message(self, format, *args):
        pass  # Disable default HTTP logging

def run_keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    print(f"Keep-alive server running on port {port} to satisfy Render.")
    server.serve_forever()

def inject_hermes_env():
    # 1. Get variables from Render (with 9router defaults as fallback)
    base_url = os.environ.get("OPENAI_API_BASE", "https://9r.ykno.ir/v1")
    api_key = os.environ.get("OPENAI_API_KEY", "")
    model_name = os.environ.get("OPENAI_MODEL_NAME", "Auto-Pilot")
    
    # 2. Trick Hermes by also setting OpenRouter variables to the same 9router values
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", api_key)
    openrouter_base = os.environ.get("OPENROUTER_API_BASE", base_url)

    # Hermes on Render uses /opt/data/.env for persistent config
    config_dir = Path("/opt/data")
    config_dir.mkdir(parents=True, exist_ok=True)
    env_file = config_dir / ".env"

    # Read existing lines and remove old conflicting entries to prevent duplicates
    lines = []
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            lines = [
                line for line in f 
                if not line.startswith((
                    "OPENAI_API_BASE=", "OPENAI_API_KEY=", "OPENAI_MODEL_NAME=",
                    "OPENROUTER_API_BASE=", "OPENROUTER_API_KEY="
                ))
            ]

    # Append the correct, fresh variables
    lines.append(f"OPENAI_API_BASE={base_url}\n")
    lines.append(f"OPENAI_API_KEY={api_key}\n")
    lines.append(f"OPENAI_MODEL_NAME={model_name}\n")
    lines.append(f"OPENROUTER_API_BASE={openrouter_base}\n")
    lines.append(f"OPENROUTER_API_KEY={openrouter_key}\n")

    # Write back to the file
    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Print a clear success message for the Render logs
    print("="*70)
    print("✅ SUCCESSFULLY INJECTED HERMES ENVIRONMENT VARIABLES")
    print(f"   API BASE: {base_url}")
    print(f"   MODEL: {model_name}")
    print(f"   ENV FILE: {env_file}")
    print("="*70)

if __name__ == "__main__":
    # Step A: Inject the environment variables BEFORE Hermes starts
    inject_hermes_env()

    # Step B: Start the Keep-Alive server in a background daemon thread
    keep_alive_thread = threading.Thread(target=run_keep_alive, daemon=True)
    keep_alive_thread.start()

    # Step C: Start the main Hermes Gateway engine
    print("🚀 Starting Hermes Gateway...")
    try:
        subprocess.run(["hermes", "gateway", "run"], check=True)
    except FileNotFoundError:
        print("❌ Error: 'hermes' command not found. Ensure hermes-agent is installed.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Critical error: Hermes gateway exited with code {e.returncode}")
        sys.exit(1)
