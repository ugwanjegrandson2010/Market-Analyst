#!/usr/bin/env python3
import subprocess, threading, webbrowser, time, os, sys
ROOT=os.path.dirname(os.path.abspath(__file__))
BACKEND=os.path.join(ROOT,'market-ai','backend')
DASHBOARD=os.path.join(ROOT,'market-ai','dashboard')
def run_backend():
    subprocess.run([sys.executable,'-m','uvicorn','main:app','--port','8000'], cwd=BACKEND)
def run_dash():
    subprocess.run([sys.executable,'-m','http.server','5173'], cwd=DASHBOARD)
threading.Thread(target=run_backend,daemon=True).start()
threading.Thread(target=run_dash,daemon=True).start()
time.sleep(3)
webbrowser.open('http://localhost:5173')
print('App running. Backend 8000, dashboard 5173. Ctrl+C to stop.')
try:
    while True: time.sleep(1)
except KeyboardInterrupt:
    pass
