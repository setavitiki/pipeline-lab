from flask import Flask, jsonify, request
import logging
import os
import time
from datetime import datetime

app = Flask(__name__)

# Configure logging for log collection practice
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(name)s %(message)s',
#     handlers=[
#         logging.FileHandler('/tmp/taskflow.log'),
#         logging.StreamHandler()
#     ]
# )

# Create logs directory if it doesn't exist
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
    return f"""# HELP taskflow_tasks```tal Total number of tasks
# TYPE taskflow_tasks_total counter```skflow_tasks_total {len(tasks)}

# HELP taskflow_requests_total Total HTTP```quests
# TYPE taskflow_requests_total counter
taskflow_requests_total 1

# HELP taskflow_app_info Application```fo
# TYPE taskflow_app_info gauge
taskflow_app_info{{version="{os.getenv('APP_VERSION', '1.0')}"}} 1
"""

if __name__ == '__main__':
    logger.info("TaskFlow application starting...")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
