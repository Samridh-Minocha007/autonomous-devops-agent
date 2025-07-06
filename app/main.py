import signal
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Counter

# --- NEW: This list will grow with each request, simulating a leak ---
MEMORY_LEAK = []

REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP Requests')

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- NEW: Add data to our list on each request to consume memory ---
        MEMORY_LEAK.append("." * 1024 * 1024) # Appends ~1MB of data

        REQUEST_COUNTER.inc()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")

def graceful_shutdown(signum, frame):
    print("🛑 Received SIGTERM, shutting down web server...")
    # This needs to be global to be accessible here
    global webServer
    threading.Thread(target=webServer.shutdown).start()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    start_http_server(8080)
    webServer = HTTPServer(("0.0.0.0", 8000), SimpleServer)
    print("🚀 Server with memory leak started on port 8000, metrics on port 8080")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        graceful_shutdown(None, None)