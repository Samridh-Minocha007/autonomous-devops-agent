import signal
import sys
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    alert_data = request.json
    print("🚨 Webhook received!")
    print(alert_data)

    problem_description = alert_data['alerts'][0]['annotations']['description']
    subprocess.run(["python", "/app/main_agent.py", problem_description])

    return "OK", 200

def graceful_shutdown(signum, frame):
    print("🛑 Flask app received SIGTERM. Cleaning up...")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, graceful_shutdown)
    app.run(host='0.0.0.0', port=5001)
