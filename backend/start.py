"""
Cross-platform startup script for all Sweet Cravings Bakery backend services.
Works on Windows, macOS, and Linux.

Usage:
    python backend/start.py
"""

import subprocess
import sys
import os
import signal
import time
import threading

# ── Colour codes ─────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable

# ── Service definitions ──────────────────────────────────────────────────────
SERVICES = [
    {"name": "user_service",    "port": 5001, "dir": "user_service"},
    {"name": "product_service", "port": 5002, "dir": "product_service"},
    {"name": "order_service",   "port": 5003, "dir": "order_service"},
    {"name": "payment_service", "port": 5004, "dir": "payment_service"},
    {"name": "api_gateway",     "port": 5050, "dir": "api_gateway"},
]

COLORS = ["\033[94m", "\033[95m", "\033[96m", "\033[93m", "\033[92m"]

processes = []


# ── Load .env manually ───────────────────────────────────────────────────────
def load_env():
    env = os.environ.copy()
    env_file = os.path.join(BASE_DIR, ".env")

    if not os.path.exists(env_file):
        return env

    with open(env_file) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip().strip('"').strip("'")

            env.setdefault(key, value)

    return env


# ── Stream logs ──────────────────────────────────────────────────────────────
def stream_output(proc, label, color):

    def reader(stream):
        for line in iter(stream.readline, b""):
            text = line.decode("utf-8", errors="replace").rstrip()
            print(f"{color}[{label}]{RESET} {text}", flush=True)

    threading.Thread(target=reader, args=(proc.stdout,), daemon=True).start()
    threading.Thread(target=reader, args=(proc.stderr,), daemon=True).start()


# ── Start service ────────────────────────────────────────────────────────────
def start_service(svc, color):

    svc_dir = os.path.join(BASE_DIR, svc["dir"])
    env = load_env()

    proc = subprocess.Popen(
        [PYTHON, "app.py"],
        cwd=svc_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1
    )

    stream_output(proc, svc["name"], color)

    print(
        f"{GREEN}✓ Started{RESET} {BOLD}{svc['name']}{RESET} "
        f"→ http://localhost:{svc['port']}",
        flush=True
    )

    return proc


# ── Shutdown handler ─────────────────────────────────────────────────────────
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
            if p.poll() is None:
                p.kill()
        except Exception:
            pass

    print(f"{GREEN}All services stopped.{RESET}")
    sys.exit(0)


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print(f"\n{BOLD}{CYAN}🍰 Sweet Cravings Bakery — Backend Services{RESET}\n")
    print(f"  Python interpreter: {PYTHON}\n")

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for i, svc in enumerate(SERVICES):
        color = COLORS[i % len(COLORS)]

        proc = start_service(svc, color)
        processes.append(proc)

        time.sleep(0.4)  # prevent port binding race

    print(f"\n{BOLD}All services running.{RESET}  Press Ctrl+C to stop.\n")

    print(f"  API Gateway → {BOLD}http://localhost:5050{RESET}")
    print(f"  Frontend    → {BOLD}http://localhost:5173{RESET}\n")

    # ── Monitor processes ────────────────────────────────────────────────────
    while True:

        for svc, proc in zip(SERVICES, processes):

            ret = proc.poll()

            if ret is not None:
                print(
                    f"{RED}[{svc['name']}] exited unexpectedly with code {ret}{RESET}"
                )

        time.sleep(2)
        
