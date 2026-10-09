"""Start the local lesson-plan web app when run as a desktop executable."""
import os
import threading
import webbrowser

from app import app


HOST = "127.0.0.1"
PORT = int(os.environ.get("LESSON_PLAN_PORT", "5000"))
URL = f"http://{HOST}:{PORT}/"


def main():
    threading.Timer(1.0, webbrowser.open, args=(URL,)).start()
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
