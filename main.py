import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cli.cli import start_cli
from gui.gui import start_gui

print("""
LinkSentry v4.0

1. CLI
2. GUI
3. API
4. Dashboard
5. Worker
""")

choice = input("Select mode: ")

if choice == "1":
    start_cli()
elif choice == "2":
    start_gui()
elif choice == "3":
    from api.server import app
    app.run(port=5000)
elif choice == "4":
    from dashboard.app import app
    app.run(port=8000)
elif choice == "5":
    from worker.worker import run_worker
    run_worker()
