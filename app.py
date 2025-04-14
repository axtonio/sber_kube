import os
from flask import Flask, request, jsonify
import logging

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
