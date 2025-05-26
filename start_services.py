#!/usr/bin/env python3
"""
Startup script for Global News Hub
Starts both Flask backend and React frontend
"""

import subprocess
import sys
import time
import os
import signal
import threading

def start_backend():
    """Start the Flask backend"""
    print("🚀 Starting Flask backend...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, 'src/api.py'],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        if backend_process.poll() is None:
            print("✅ Flask backend started successfully on http://localhost:5000")
            return backend_process
        else:
            stdout, stderr = backend_process.communicate()
            print(f"❌ Flask backend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Flask backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("🚀 Starting React frontend...")
    try:
        frontend_process = subprocess.Popen(
            ['npm', 'start'],
            cwd=os.path.join(os.getcwd(), 'frontend'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        if frontend_process.poll() is None:
            print("✅ React frontend started successfully on http://localhost:3000")
            return frontend_process
        else:
            stdout, stderr = frontend_process.communicate()
            print(f"❌ React frontend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting React frontend: {e}")
        return None

def main():
    """Main startup function"""
    print("🌍 Global News Hub - Starting Services")
    print("=" * 50)
    
    processes = []
    
    try:
        # Start backend
        backend = start_backend()
        if backend:
            processes.append(backend)
        
        # Start frontend
        frontend = start_frontend()
        if frontend:
            processes.append(frontend)
        
        if not processes:
            print("❌ No services started successfully")
            return
        
        print("\n🎉 Services started successfully!")
        print("📊 Backend API: http://localhost:5000")
        print("🌐 Frontend UI: http://localhost:3000")
        print("\nPress Ctrl+C to stop all services...")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
                # Check if processes are still running
                for process in processes[:]:
                    if process.poll() is not None:
                        print(f"⚠️  Process {process.pid} has stopped")
                        processes.remove(process)
                
                if not processes:
                    print("❌ All processes have stopped")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            
    except Exception as e:
        print(f"❌ Error in main: {e}")
    
    finally:
        # Clean up processes
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        print("✅ All services stopped")

if __name__ == '__main__':
    main() 