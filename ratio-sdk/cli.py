import os
import sys
import argparse
import subprocess
import uvicorn
from pyfiglet import Figlet

def start_node(port=8000):
    f = Figlet(font='slant')
    print(f.renderText('RATIO Node'))
    print(f"🚀 Starting Cloudless Governance Node on port {port}...")
    print("💡 Connect your dashboard to this node to perform audits for FREE.")
    
    # Change to backend directory and start the server
    backend_dir = os.path.join(os.path.dirname(__file__), "../backend")
    os.environ["PYTHONPATH"] = f"{backend_dir}:{os.environ.get('PYTHONPATH', '')}"
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

def main():
    parser = argparse.ArgumentParser(description="RATIO Governance Platform SDK")
    subparsers = parser.add_subparsers(dest="command")

    # Start Node
    start_parser = subparsers.add_parser("start", help="Start the local governance node")
    start_parser.add_argument("--port", type=int, default=8000, help="Port to run the node on")

    # Tunnel Guide
    tunnel_parser = subparsers.add_parser("tunnel", help="Show instructions for cloud dashboard connection")

    args = parser.parse_args()

    if args.command == "start":
        start_node(args.port)
    elif args.command == "tunnel":
        print("\n--- RATIO CLOUDLESS TUNNEL GUIDE ---")
        print("To connect the Cloud Dashboard (GitHub Pages) to this Local Node:")
        print("1. Install ngrok: brew install ngrok/ngrok/ngrok")
        print(f"2. Start tunnel: ngrok http {args.port or 8000}")
        print("3. Copy the HTTPS URL from ngrok and paste it into Dashboard Settings (⚙️).")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
