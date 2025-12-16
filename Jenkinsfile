pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "khanhnh/iris-ml-api"
        DOCKER_TAG = "${BUILD_NUMBER}"
        // Đảm bảo ID này đã tồn tại trong Jenkins Credentials
        DOCKER_CREDENTIALS_ID = "khanhjt" 
    }

    // --- SỬA LỖI 1: Thêm block stages bao quanh ---
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
                    
                    # --- SỬA LỖI 2: pip install . thay vì -r pyproject.toml ---
                    # Cài đặt package hiện tại ở chế độ editable hoặc cài thường
                    # Nếu cần cài thêm thư viện test (pytest), hãy đảm bảo chúng nằm trong dependencies
                    pip install . 
                    
                    # Hoặc nếu bạn có file requirements.txt được generate từ pyproject.toml:
                    # pip install -r requirements.txt
                '''
            }
        }

        stage('Train model') {
            steps {
                echo 'Train ML model...'
                sh '''
                    . venv/bin/activate
                    cd src
                    python train_model.py
                    cd ..
                '''
            }
        }

        stage('Test model') {
            steps {
                echo 'Testing model training and predictions...'
                sh '''
                    . venv/bin/activate
                    # Đảm bảo pytest đã được cài ở bước Setup
                    pytest tests/test_model.py -v --tb=short
                '''
            }
        }

        stage('Test API') {
            steps {
                echo 'Testing FastAPI application...'
                sh '''
                    . venv/bin/activate
                    pytest tests/test_app.py -v --tb=short
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