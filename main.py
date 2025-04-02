import os
import subprocess
import threading
import time
import sys
import signal

def run_frontend():
    """Run the Vue.js frontend development server"""
    print("Starting Vue.js frontend...")
    os.chdir("frontend")
    # Use npm run serve for development mode
    frontend_process = subprocess.Popen(
        "npm run serve", 
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Print output from the frontend process
    for line in frontend_process.stdout:
        print(f"[FRONTEND] {line.strip()}")
    
    frontend_process.wait()
    print("Frontend process has stopped.")

def run_backend():
    """Run the Flask backend server"""
    print("Starting Flask backend...")
    os.chdir("backend")
    # Set Flask development mode
    os.environ["FLASK_ENV"] = "development"
    
    # Run the Flask app
    backend_process = subprocess.Popen(
        "python app.py",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Print output from the backend process
    for line in backend_process.stdout:
        print(f"[BACKEND] {line.strip()}")
    
    backend_process.wait()
    print("Backend process has stopped.")

def handle_exit(signum, frame):
    """Handle exit signals to ensure clean shutdown"""
    print("\nShutting down servers...")
    sys.exit(0)

def main():
    # Register signal handlers for clean exit
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    # Store original directory
    original_dir = os.getcwd()
    
    try:
        # Create and start frontend thread
        frontend_thread = threading.Thread(target=run_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()
        
        # Create and start backend thread
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        print("Both servers are now running!")
        print("Frontend will be available at: http://localhost:8080")
        print("Backend API will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop both servers.")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
            # Check if either thread has died
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
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()