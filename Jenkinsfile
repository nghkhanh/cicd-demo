pipeline {
    agent any
    
    enviroment {
        DOCKER_IMAGE = "khanhnh/iris-ml-api"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = "hehe"
    }

    statge('Checkout') {
        steps {
            echo "Checking out code from Github"
            checkout scm
        }
    }

    statge('Setup python environment') {
        steps {
            echo 'Settings up python environment'
            sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r pyproject.toml
            '''
        }
    }

    statge('Train model') {
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
    statge('Test model') {
        steps {
            echo 'Testing model training and predictions...'
            sh '''
                . venv/bin/activate
                pytest tests/test_model.py -v --tb=short
            '''
        }
    }

    statge('Test API') {
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
            sh '''
                docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                docker rmi ${DOCKER_IMAGE}:latest || true
                rm -rf venv
            '''
        }
    }

    post {
        success {
            echo "Pipeline completed successfully"
            echo "Docker image pushed: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo 'Pipeline failed!'
        }
        alway {
            echo 'Cleaning workspace...'
            cleanWs()
        }
    }
}
# test webhook
