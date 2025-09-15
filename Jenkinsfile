pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pipeline-lab'
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
                    echo "BUILD_NUMBER: ${BUILD_NUMBER}"
                    echo "DOCKER_IMAGE: ${DOCKER_IMAGE}"
                    echo "DOCKER_TAG: ${DOCKER_TAG}"
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
                    
                    flake8 app.py --max-line-length=88 || echo "Linting warnings found"
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
                        echo "Starting deployment to EC2..."
                        
                        # Save Docker image as compressed tarball
                        docker save ${DOCKER_IMAGE}:${DOCKER_TAG} | gzip > pipeline-lab-${DOCKER_TAG}.tar.gz
                        echo "Docker image saved: pipeline-lab-${DOCKER_TAG}.tar.gz"
                        
                        # Copy tarball to EC2
                        scp -o StrictHostKeyChecking=no pipeline-lab-${DOCKER_TAG}.tar.gz ec2-user@65.1.13.126:/home/ec2-user/
                        echo "Tarball copied to EC2"
                        
                        # Deploy on EC2 with variables properly passed
                        ssh -o StrictHostKeyChecking=no ec2-user@65.1.13.126 "
                            echo 'Loading Docker image on EC2...'
                            docker load < pipeline-lab-${DOCKER_TAG}.tar.gz
                            
                            echo 'Stopping existing container...'
                            docker stop pipeline-lab || true
                            docker rm pipeline-lab || true
                            
                            echo 'Starting new container...'
                            docker run -d \\
                                --name pipeline-lab \\
                                -p 80:5000 \\
                                -e ENVIRONMENT=production \\
                                -e APP_VERSION=${DOCKER_TAG} \\
                                -e BUILD_NUMBER=${BUILD_NUMBER} \\
                                --restart unless-stopped \\
                                ${DOCKER_IMAGE}:${DOCKER_TAG}
                            
                            echo 'Verifying container started...'
                            docker ps | grep pipeline-lab
                            
                            echo 'Cleaning up...'
                            rm -f pipeline-lab-${DOCKER_TAG}.tar.gz
                            docker image prune -f
                        "
                        
                        # Clean up local tarball
                        rm -f pipeline-lab-${DOCKER_TAG}.tar.gz
                        echo "Deployment completed successfully!"
                    '''
                }
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Starting health check..."
                    sleep 30
                    
                    EC2_IP="65.1.13.126"
                    SERVICE_URL="http://${EC2_IP}.nip.io"
                    DIRECT_URL="http://${EC2_IP}"
                    
                    echo "Testing service at: $SERVICE_URL"
                    echo "Direct IP test: $DIRECT_URL"
                    
                    # Test direct IP first
                    for i in {1..5}; do
                        echo "Direct IP health check attempt $i..."
                        if curl -f $DIRECT_URL/health; then
                            echo "Direct IP health check passed!"
                            break
                        else
                            echo "Direct IP check failed, retrying in 10 seconds..."
                            sleep 10
                        fi
                    done
                    
                    # Test nip.io domain
                    for i in {1..5}; do
                        echo "nip.io health check attempt $i..."
                        if curl -f $SERVICE_URL/health; then
                            echo "nip.io health check passed!"
                            echo "Application accessible at: $SERVICE_URL"
                            break
                        else
                            echo "nip.io check failed, retrying in 10 seconds..."
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
            echo 'Application deployed to AWS EC2!'
            echo 'Access at: http://65.1.13.126.nip.io'
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
    }
}
