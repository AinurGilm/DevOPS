pipeline {
    agent any // Запускать пайплайн на любом доступном воркере Дженкинса

    environment {
        // Имя вашего образа на DockerHub
        DOCKER_IMAGE = "ainurgilm/weight-loss-web:latest"
        // ID учетных данных DockerHub, сохраненных в Jenkins
        DOCKER_CREDS = "dockerhub-credentials-id" 
    }

    stages {
        stage('1. Checkout') {
            steps {
                // Скачиваем актуальный код из вашего Git-репозитория
                checkout scm
            }
        }

        stage('2. Install Dependencies & Lint') {
            steps {
                echo 'Установка зависимостей проекта...'
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('3. Run Auto-Tests (PyTest)') {
            steps {
                echo 'Запуск автоматических тестов API и модели...'
                // Запускаем тесты. Если хоть один упадет, пайплайн прервется
                sh './venv/bin/pytest tests/'
            }
        }

        stage('4. Build Docker Image') {
            steps {
                echo 'Тесты пройдены! Собираем новый Production Docker-образ...'
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('5. Push to DockerHub') {
            steps {
                echo 'Авторизуемся и отправляем образ в реестр...'
                // Безопасно подставляем логин/пароль от вашего DockerHub из секретов Jenkins
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Пайплайн успешно завершен! Образ обновлен в DockerHub.'
        }
        failure {
            echo '❌ Сборка упала. Проверьте логи этапа, на котором произошел сбой.'
        }
    }
}