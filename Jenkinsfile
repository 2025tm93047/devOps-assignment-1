pipeline {
    agent any
    options { timestamps(); skipDefaultCheckout(true) }
    environment { IMAGE_NAME = 'aceest-fitness-devops'; CONTAINER_NAME = 'aceest-fitness-jenkins-smoke' }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install and Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m venv .venv'
                        sh '.venv/bin/python -m pip install -r requirements.txt'
                        sh '.venv/bin/python -m pytest -q'
                    } else {
                        bat 'py -3 -m venv .venv'
                        bat '.venv/Scripts/python.exe -m pip install -r requirements.txt'
                        bat '.venv/Scripts/python.exe -m pytest -q'
                    }
                }
            }
        }
        stage('Docker Build and Smoke Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    script {
                        if (isUnix()) {
                            sh "docker build --tag ${env.IMAGE_NAME}:${env.BUILD_NUMBER} ."
                            sh "docker run --detach --rm --name ${env.CONTAINER_NAME} --publish 5099:5000 ${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
                            sh 'python3 ci/health_check.py http://127.0.0.1:5099/healthz'
                        } else {
                            bat 'docker build --tag %IMAGE_NAME%:%BUILD_NUMBER% .'
                            bat 'docker run --detach --rm --name %CONTAINER_NAME% --publish 5099:5000 %IMAGE_NAME%:%BUILD_NUMBER%'
                            bat 'py -3 ci/health_check.py http://127.0.0.1:5099/healthz'
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                if (isUnix()) {
                    sh 'docker rm --force $CONTAINER_NAME >/dev/null 2>&1 || true'
                    sh 'docker image rm $IMAGE_NAME:$BUILD_NUMBER >/dev/null 2>&1 || true'
                } else {
                    bat 'docker rm --force %CONTAINER_NAME% >NUL 2>&1 || exit /b 0'
                    bat 'docker image rm %IMAGE_NAME%:%BUILD_NUMBER% >NUL 2>&1 || exit /b 0'
                }
            }
        }
    }
}
