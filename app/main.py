import signal
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Counter

REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP Requests')

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        REQUEST_COUNTER.inc()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")

def graceful_shutdown(signum, frame):
    print("🛑 Received SIGTERM, shutting down web server...")
    threading.Thread(target=webServer.shutdown).start()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    start_http_server(8080)
    webServer = HTTPServer(("0.0.0.0", 8000), SimpleServer)
    print("🚀 Server started on port 8000, metrics on port 8080")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        graceful_shutdown(None, None)
