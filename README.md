# TaskFlow

A production-grade task management API built with Flask, demonstrating modern DevOps practices including containerization, automated CI/CD pipelines, and comprehensive monitoring.

## Architecture Overview

```
GitHub Repository
        |
        | (Webhook)
        v
Jenkins CI/CD Pipeline
        |
        | (Build, Test, Deploy)
        v
AWS EC2 Production Environment
        |
        | (Metrics)
        v
Prometheus + Grafana Monitoring Stack
```

## Project Overview

TaskFlow is a RESTful API application designed to demonstrate enterprise-level DevOps automation practices. The project implements a complete software delivery pipeline from source control to production deployment with real-time monitoring and observability.

## Technology Stack

**Application Layer**
- Python 3.11
- Flask Web Framework
- Docker Containerization

**Infrastructure & Deployment**
- Jenkins CI/CD Pipeline
- AWS EC2 Cloud Infrastructure
- Docker Container Orchestration
- GitHub Webhooks Integration

**Monitoring & Observability**
- Prometheus Metrics Collection
- Grafana Dashboard Visualization
- Application Performance Monitoring

**Development Practices**
- Git Version Control with GitFlow
- Automated Testing and Linting
- Infrastructure as Code
- Security Best Practices

## Features

### API Capabilities
- RESTful task management endpoints
- Health check and status monitoring
- Prometheus metrics exposition
- JSON-based request/response handling

### DevOps Automation
- Automated build and deployment pipeline
- Zero-downtime deployments
- Container-based application delivery
- Real-time application monitoring
- Automated testing and code quality checks

## API Documentation

### Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | / | Application information | JSON with app details |
| GET | /health | Health check status | JSON with health status |
| GET | /tasks | Retrieve all tasks | JSON array of tasks |
| POST | /tasks | Create new task | JSON with created task |
| GET | /metrics | Prometheus metrics | Prometheus exposition format |

### Example Usage

**Create a new task:**
```bash
curl -X POST http://your-domain/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete project documentation"}'
```

**Retrieve all tasks:**
```bash
curl http://your-domain/tasks
```

**Check application health:**
```bash
curl http://your-domain/health
```

## Quick Start

### Prerequisites
- Docker 28.0+
- Python 3.12+
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/taskflow-app.git
cd taskflow-app
```

2. Build the Docker image:
```bash
docker build -f docker/Dockerfile -t taskflow-app .
```

3. Run the application:
```bash
docker run -d -p 5000:5000 --name taskflow-app taskflow-app
```

4. Verify the deployment:
```bash
curl http://localhost:5000/health
```

## Production Deployment

The application is automatically deployed to AWS EC2 through a Jenkins CI/CD pipeline that triggers on code commits to the develop branch.

### Deployment Process
1. Code push to GitHub triggers webhook
2. Jenkins pipeline executes automated build and test procedures
3. Docker image is created and tagged with build number
4. Image is deployed to AWS EC2 production environment
5. Health checks verify successful deployment
6. Monitoring systems begin collecting application metrics

### Monitoring Access
- **Prometheus**: http://monitoring-host:9090
- **Grafana**: http://monitoring-host:3000

## Monitoring and Metrics

The application exposes comprehensive metrics for monitoring and observability:

### Available Metrics
- `taskflow_requests_total`: HTTP request counter with method and endpoint labels
- `taskflow_request_latency_seconds`: Request response time histogram
- `taskflow_tasks_total`: Total number of tasks created
- `taskflow_app_info`: Application version and build information

### Performance Monitoring
Real-time dashboards provide visibility into:
- Request throughput and response times
- Application health and availability
- Task creation patterns and usage metrics
- System resource utilization

## Development Practices

### Code Quality
- Automated linting with flake8
- Code review process through pull requests
- Automated testing in CI/CD pipeline
- Security scanning and vulnerability assessment

### Infrastructure Management
- Infrastructure as Code principles
- Containerized application deployment
- Automated environment provisioning
- Configuration management through environment variables

### Security Implementation
- Non-root container execution
- Secure credential management
- Network security group configuration
- SSL/TLS encryption for data in transit

## Project Structure

```
taskflow-app/
├── src/
│   ├── app.py              # Main Flask application
│   └── requirements.txt    # Python dependencies
├── docker/
│   └── Dockerfile          # Container build instructions
├── Jenkinsfile            # CI/CD pipeline definition
└── README.md              # Project documentation
```

## Environment Configuration

The application supports environment-specific configuration through environment variables:

- `ENVIRONMENT`: Deployment environment (development/production)
- `APP_VERSION`: Application version identifier
- `BUILD_NUMBER`: CI/CD build number
- `PORT`: Application listening port (default: 5000)

## Continuous Integration/Continuous Deployment

The Jenkins pipeline implements the following stages:

1. **Source Code Checkout**: Retrieves latest code from GitHub
2. **Code Quality Analysis**: Executes linting and static analysis
3. **Automated Testing**: Runs application test suite
4. **Container Build**: Creates Docker image with build tagging
5. **Production Deployment**: Deploys container to AWS EC2
6. **Health Verification**: Confirms successful deployment
7. **Monitoring Integration**: Enables metrics collection

## Contributing

This project follows standard software development practices:

1. Fork the repository
2. Create a feature branch from develop
3. Implement changes with appropriate tests
4. Submit pull request for code review
5. Automated pipeline validates changes
6. Merge to develop branch triggers deployment

## License

This project is licensed under the GPL-3.0 license.

## Technical Support

For technical inquiries and support, please refer to the project documentation or submit issues through the appropriate channels.

## Author

Shaun T