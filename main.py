# ----- REQUIRED IMPORTS -----

import os
import subprocess
import threading
import time
import sys
import signal

# ----- HELPER FUNCTIONS -----

def run_frontend():
    print("Starting Vue.js frontend...")
    os.chdir("frontend")
    frontend_process = subprocess.Popen(
        "npm run serve", 
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    for line in frontend_process.stdout: # for logging and debugging
        print(f"[FRONTEND] {line.strip()}")
    frontend_process.wait()
    print("Frontend process has stopped.")

def run_backend():
    print("Starting Flask backend...")
    os.chdir("backend")
    os.environ["FLASK_ENV"] = "development"
    backend_process = subprocess.Popen(
        "python3 app.py",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    for line in backend_process.stdout:
        print(f"[BACKEND] {line.strip()}")
    backend_process.wait()
    print("Backend process has stopped.")

def handle_exit(signum, frame):
    print("\nShutting down servers...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    original_dir = os.getcwd()
    try:
        frontend_thread = threading.Thread(target=run_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        print("Both servers are now running!")
        print("Frontend will be available at: http://localhost:8080")
        print("Backend API will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop both servers.")
        while True:
            time.sleep(1)
            if not frontend_thread.is_alive() and not backend_thread.is_alive():
                print("Both servers have stopped. Exiting.")
                break
            elif not frontend_thread.is_alive():
                print("Frontend server has stopped unexpectedly.")
                break
            elif not backend_thread.is_alive():
                print("Backend server has stopped unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nShutting down servers...")
    finally:
        os.chdir(original_dir)

# ----- MAIN EXECUTION CODE -----

if __name__ == "__main__":
    main()