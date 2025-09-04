from flask import Flask, jsonify, request, Response
import logging
import os
import time
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Configure logging
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'taskflow.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# In-memory task storage
tasks = []

# Prometheus metrics
REQUEST_COUNT = Counter('taskflow_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('taskflow_request_latency_seconds', 'HTTP request latency in seconds', ['method', 'endpoint'])
TASK_COUNT = Counter('taskflow_tasks_total', 'Total number of tasks created')
APP_INFO = Counter('taskflow_app_info', 'Application info', ['version'])

# Initialize app info metric
APP_INFO.labels(version=os.getenv('APP_VERSION', '1.0')).inc()

@app.before_request
def before_request():
    request.start_time = time.time()
    endpoint = request.endpoint if request.endpoint else 'unknown'
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()

@app.after_request
def after_request(response):
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        endpoint = request.endpoint if request.endpoint else 'unknown'
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(duration)
    return response

@app.route('/')
def home():
    logger.info(f"Home page accessed from {request.remote_addr}")
    return jsonify({
        "message": "TaskFlow Application",
        "version": os.getenv('APP_VERSION', '1.0'),
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "total_tasks": len(tasks)
    })

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        task_data = request.get_json()
        task = {
            'id': len(tasks) + 1,
            'title': task_data.get('title', 'Untitled'),
            'created_at': datetime.now().isoformat()
        }
        tasks.append(task)
        TASK_COUNT.inc()  # Increment task counter
        logger.info(f"New task created: {task['title']}")
        return jsonify({"status": "created", "task": task}), 201
    
    logger.info(f"Tasks retrieved, total: {len(tasks)}")
    return jsonify({"tasks": tasks})

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": os.getenv('APP_VERSION', '1.0')
    })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    logger.info("TaskFlow application starting...")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
