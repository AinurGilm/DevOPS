pipeline {
    agent any
    stages {
        stage('1. Clean & Checkout') {
            steps {
                // Очистка только старых файлов, но сохранение структуры git
                cleanWs()
                checkout scm
            }
        }
        stage('2. Build Docker Image') {
            steps {
                echo "Собираем Docker-образ..."
                // Docker сам использует кэш слоев, если Dockerfile написан верно
                sh 'docker build -t ainurgilm/weight-loss-web:latest .'
            }
        }
        stage('3. Push to DockerHub') {
            steps {
                echo "Pushing to DockerHub..."
                sh 'docker push ainurgilm/weight-loss-web:latest'
            }
        }
    }
    post {
        failure {
            echo "❌ Сборка упала. Проверьте логи."
        }
    }
}