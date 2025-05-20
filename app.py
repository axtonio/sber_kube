import os
from flask import Flask, request, jsonify, Response
import logging

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
PORT = int(os.environ.get('PORT', 5000))
WELCOME_MESSAGE = os.environ.get(
    'WELCOME_MESSAGE', 'Welcome to the custom app')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/app.log')
    ]
)
logger = logging.getLogger(__name__)

# --- PROMETHEUS METRICS ---
REQUEST_COUNT = Counter(
    'flask_app_requests_total', 'Total App HTTP Requests', ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'flask_app_request_latency_seconds', 'Flask Request latency', ['endpoint']
)

from time import time

@app.before_request
def before_request():
    request.start_time = time()

@app.after_request
def after_request(response):
    latency = time() - getattr(request, 'start_time', time())
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.path).observe(latency)
    return response

@app.route('/', methods=['GET'])
def welcome():
    logger.info("Welcome endpoint called")
    return WELCOME_MESSAGE

@app.route('/status', methods=['GET'])
def status():
    logger.info("Status endpoint called")
    return jsonify({"status": "ok"})

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    message = data.get('message', '')
    logger.info(f"Received log message: {message}")

    with open('/app/logs/app.log', 'a') as f:
        f.write(f"{message}\n")

    return jsonify({"status": "logged"})

@app.route('/logs', methods=['GET'])
def get_logs():
    logger.info("Logs endpoint called")
    try:
        with open('/app/logs/app.log', 'r') as f:
            logs = f.read()
        return logs
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return jsonify({"error": str(e)}), 500

# --- METRICS ENDPOINT ---
@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)