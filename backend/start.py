"""
Cross-platform startup script for all 5 Sweet Cravings Bakery backend services.
Works identically on Windows, macOS, and Linux.

Usage:  python backend/start.py   (from project root)
        or called automatically by: npm run dev
"""

import subprocess
import sys
import os
import signal
import time
import threading

# ── Colour codes (work on Mac/Linux; Windows 10+ with ANSI support) ──────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# ── Service definitions: (name, port, working_dir_relative_to_this_file) ─────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVICES = [
    {"name": "user_service",    "port": 5001, "dir": "user_service"},
    {"name": "product_service", "port": 5002, "dir": "product_service"},
    {"name": "order_service",   "port": 5003, "dir": "order_service"},
    {"name": "payment_service", "port": 5004, "dir": "payment_service"},
    {"name": "api_gateway",     "port": 5050, "dir": "api_gateway"},
]

# sys.executable gives the EXACT python interpreter running this script
# — no python vs python3 ambiguity across platforms
PYTHON = sys.executable

processes = []


def stream_output(proc, label, color):
    """Stream stdout and stderr from a subprocess with a prefixed label."""
    def _read(stream):
        for line in iter(stream.readline, b""):
            text = line.decode("utf-8", errors="replace").rstrip()
            print(f"{color}[{label}]{RESET} {text}", flush=True)
    t1 = threading.Thread(target=_read, args=(proc.stdout,), daemon=True)
    t2 = threading.Thread(target=_read, args=(proc.stderr,), daemon=True)
    t1.start()
    t2.start()


def start_service(svc, color):
    svc_dir = os.path.join(BASE_DIR, svc["dir"])
    
    # Load .env from backend/ into the subprocess environment
    env = os.environ.copy()
    env_file = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    env.setdefault(key.strip(), val.strip())

    proc = subprocess.Popen(
        [PYTHON, "app.py"],
        cwd=svc_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stream_output(proc, svc["name"], color)
    print(f"{GREEN}✓ Started{RESET} {BOLD}{svc['name']}{RESET} → http://localhost:{svc['port']}")
    return proc


COLORS = ["\033[94m", "\033[95m", "\033[96m", "\033[93m", "\033[92m"]


def shutdown(signum=None, frame=None):
    print(f"\n{YELLOW}Shutting down all services…{RESET}")
    for p in processes:
        try:
            p.terminate()
        except Exception:
            pass
    time.sleep(1)
    for p in processes:
        try:
            p.kill()
        except Exception:
            pass
    print(f"{GREEN}All services stopped.{RESET}")
    sys.exit(0)


if __name__ == "__main__":
    print(f"\n{BOLD}{CYAN}🍰 Sweet Cravings Bakery — Backend Services{RESET}\n")
    print(f"  Python interpreter: {PYTHON}\n")

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for i, svc in enumerate(SERVICES):
        color = COLORS[i % len(COLORS)]
        proc = start_service(svc, color)
        processes.append(proc)
        time.sleep(0.3)  # small stagger to avoid port-bind races

    print(f"\n{BOLD}All services running.{RESET}  Press Ctrl+C to stop.\n")
    print(f"  API Gateway → {BOLD}http://localhost:5050{RESET}")
    print(f"  Frontend    → {BOLD}http://localhost:5173{RESET}  (Vite dev server)\n")

    # Keep alive — wait for any process to die unexpectedly
    while True:
        for svc, proc in zip(SERVICES, processes):
            ret = proc.poll()
            if ret is not None:
                print(f"{RED}[{svc['name']}] exited with code {ret}{RESET}")
        time.sleep(2)
