import os
import sys
import uvicorn
import webbrowser
from pyfiglet import Figlet

def start_hub():
    # Setup Paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    
    # Pre-checks: Ensure Frontend exists
    frontend_path = os.path.join(root_dir, "frontend", "dashboard")
    if not os.path.exists(frontend_path):
        print(f"❌ CRITICAL ERROR: Frontend not found at {frontend_path}")
        return

    # Set PYTHONPATH to both root and backend for smooth imports
    sys.path.insert(0, root_dir)
    sys.path.insert(0, backend_dir)
    
    f = Figlet(font='slant')
    print(f.renderText('RATIO Hub'))
    
    print("--- NEURAL PIPELINE STARTUP ---")
    print(f"📍 Root: {root_dir}")
    print(f"📍 Dashboard: {frontend_path}")
    print("--- SUCCESS ---")
    
    url = "http://localhost:8000/dashboard"
    print(f"\n🚀 Hub is Active! CLICK TO OPEN:\n🔗 {url}")
    print("\n[NOTE] If the score is not showing, ensure your Gemini API is active in model_adapter.py.")
    
    # Auto-open in browser
    webbrowser.open(url)
    
    # Start the server (pointing to app/main.py inside backend)
    # Since we are in the root, and we added backend to sys.path, we use app.main:app
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start_hub()
