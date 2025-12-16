pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "khanhnh/iris-ml-api"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = "khanhjt" 
    }

    stages { 
        stage('Checkout') {
            steps {
                echo "Checking out code from Github"
                checkout scm
            }
        }

        stage('Setup python environment') {
            steps {
                echo 'Settings up python environment'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install . 
                    
                '''
            }
        }

        stage('Train model') {
            steps {
                echo 'Train ML model...'
                sh '''
                    . venv/bin/activate
                    python src/train_model.py
                '''
            }
        }

        stage('Test model') {
            steps {
                echo 'Testing model training and predictions...'
                sh '''
                    . venv/bin/activate
                    pip install pytest
                    pytest test/test_model.py -v --tb=short
                '''
            }
        }

        stage('Test API') {
            steps {
                echo 'Testing FastAPI application...'
                sh '''
                    . venv/bin/activate
                    pip install pytest
                    pytest test/test_app.py -v --tb=short
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Push to Docker hub'
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }

        stage('Clean up') {
            steps {
                echo 'Cleaning up...'
                // Dùng || true để tránh fail pipeline nếu không có ảnh để xóa
                sh '''
                    docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                    docker rmi ${DOCKER_IMAGE}:latest || true
                    rm -rf venv
                '''
            }
        }
    } // Kết thúc block stages

    post {
        success {
            echo "Pipeline completed successfully"
            echo "Docker image pushed: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo 'Pipeline failed!'
        }
        // --- SỬA LỖI 3: alway -> always ---
        always {
            echo 'Cleaning workspace...'
            cleanWs()
        }
    }
}