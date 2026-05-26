pipeline {
    agent any 

    options {
        // Отключаем автоматический ломающийся чекаут Jenkins
        skipDefaultCheckout()
    }

    environment {
        DOCKER_IMAGE = "ainurgilm/weight-loss-web:latest"
        DOCKER_CREDS = "dockerhub-credentials-id" 
    }

    stages {
        stage('1. Clean & Checkout') {
            steps {
                echo 'Принудительная очистка рабочей папки и свежий клон репозитория...'
                // Физически стирает всё внутри текущего workspace сборки
                deleteDir() 
                
                // Делаем чистый клон репозитория напрямую
                sh "git clone https://github.com/AinurGilm/DevOPS.git ."
                sh "git checkout master"
            }
        }

        stage('2. Build Docker Image & Run Tests') {
            steps {
                echo 'Собираем Production Docker-образ и автоматически прогоняем тесты...'
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