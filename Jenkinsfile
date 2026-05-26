pipeline {
    agent any 

    environment {
        DOCKER_IMAGE = "ainurgilm/weight-loss-web:latest"
        DOCKER_CREDS = "dockerhub-credentials-id" 
    }

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
            }
        }

        stage('2. Build Docker Image & Run Tests') {
            steps {
                echo 'Собираем Production Docker-образ и автоматически прогоняем тесты внутри него...'
                // Docker сам запустит pytest из Dockerfile. Если тесты упадут — сборка завалится здесь.
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('3. Push to DockerHub') {
            steps {
                echo 'Авторизуемся и отправляем проверенный образ в реестр...'
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Пайплайн успешно завершен! Образ проверен тестами и обновлен в DockerHub.'
        }
        failure {
            echo '❌ Сборка упала. Проверьте логи.'
        }
    }
}