pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'taskflow-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Current branch: ${GIT_BRANCH}"'
                sh 'echo "Commit: ${GIT_COMMIT}"'
            }
        }
        
        stage('Lint & Test') {
            steps {
                sh '''
                    cd src
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install flake8
                    
                    # Basic linting
                    flake8 app.py --max-line-length=88 || echo "Linting warnings found"
                    
                    # Basic import test
                    python -c "import app; print('App imports successfully')"
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -f docker/Dockerfile -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    docker images | grep ${DOCKER_IMAGE}
                '''
            }
        }
        
        stage('Deploy to Kubernetes') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh '''
                    # Load image into minikube
                    minikube image load ${DOCKER_IMAGE}:${DOCKER_TAG}
                    
                    # Update deployment with new image
                    kubectl set image deployment/taskflow-app taskflow=${DOCKER_IMAGE}:${DOCKER_TAG}
                    
                    # Wait for rollout to complete
                    kubectl rollout status deployment/taskflow-app --timeout=300s
                    
                    # Verify deployment
                    kubectl get pods -l app=taskflow
                '''
            }
        }
        
        stage('Health Check') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh '''
                    # Wait for service to be ready
                    sleep 30
                    
                    # Get service URL and test health
                    SERVICE_URL=$(minikube service taskflow-service --url)
                    echo "Testing service at: $SERVICE_URL"
                    
                    # Health check with retry
                    for i in {1..5}; do
                        if curl -f $SERVICE_URL/health; then
                            echo "Health check passed!"
                            break
                        else
                            echo "Health check failed, retrying in 10 seconds..."
                            sleep 10
                        fi
                    done
                '''
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f || true'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
    }
}
