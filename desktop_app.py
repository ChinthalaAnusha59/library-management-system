import threading
import time
import webview
from app import app


def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)


flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

time.sleep(2)

window = webview.create_window(
    "Library Management System",
    "http://127.0.0.1:5000",
    width=1200,
    height=800
)

webview.start()