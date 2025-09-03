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

        stage('Debug Environment') {
            steps {
                sh '''
                    echo "=== Environment Debug ==="
                    echo "GIT_BRANCH: ${GIT_BRANCH}"
                    echo "BRANCH_NAME: ${BRANCH_NAME}"
                    echo "BUILD_NUMBER: ${BUILD_NUMBER}"
                    echo "DOCKER_IMAGE: ${DOCKER_IMAGE}"
                    echo "DOCKER_TAG: ${DOCKER_TAG}"
                    echo "Current working directory: $(pwd)"
                    echo "Git status: $(git status --porcelain)"
                '''
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
        
        stage('Deploy to AWS EC2') {
            steps {
                sshagent(['ec2-deploy-key']) {
                    sh '''
                        # Build and save Docker image as tar
                        docker save ${DOCKER_IMAGE}:${DOCKER_TAG} | gzip > taskflow-${DOCKER_TAG}.tar.gz
                        
                        # Copy image to EC2
                        scp -o StrictHostKeyChecking=no taskflow-${DOCKER_TAG}.tar.gz ubuntu@13.60.25.113:/home/ubuntu/
                        
                        # Deploy on EC2
                        ssh -o StrictHostKeyChecking=no ubuntu@13.60.25.113 "
                            # Load Docker image
                            docker load < taskflow-${DOCKER_TAG}.tar.gz
                            
                            # Stop existing container if running
                            docker stop taskflow-app || true
                            docker rm taskflow-app || true
                            
                            # Run new container
                            docker run -d \\
                                --name taskflow-app \\
                                -p 80:5000 \\
                                -e ENVIRONMENT=production \\
                                -e APP_VERSION=${DOCKER_TAG} \\
                                -e BUILD_NUMBER=${BUILD_NUMBER} \\
                                --restart unless-stopped \\
                                ${DOCKER_IMAGE}:${DOCKER_TAG}
                            
                            # Clean up old images
                            docker image prune -f
                            
                            # Remove tar file
                            rm -f taskflow-${DOCKER_TAG}.tar.gz
                        "
                        
                        # Clean up local tar file
                        rm -f taskflow-${DOCKER_TAG}.tar.gz
                    '''
                }
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    # Wait for application to start
                    sleep 30
                    
                    # Health check using nip.io domain
                    EC2_IP="13.60.25.113"
                    SERVICE_URL="http://${EC2_IP}.nip.io"
                    echo "Testing service at: $SERVICE_URL"
                    
                    # Health check with retry
                    for i in {1..10}; do
                        if curl -f $SERVICE_URL/health; then
                            echo "Health check passed!"
                            echo "Application accessible at: $SERVICE_URL"
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
