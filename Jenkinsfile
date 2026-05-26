pipeline {
    agent any 

    options {
        skipDefaultCheckout()
    }

    environment {
        DOCKER_IMAGE = "ainurgilm/weight-loss-web:latest"
    }

    stages {
        stage('1. Clean & Checkout') {
            steps {
                echo 'Принудительная очистка рабочей папки и свежий клон репозитория...'
                deleteDir() 
                sh "git clone https://github.com/AinurGilm/DevOPS.git ."
                sh "git checkout master"
            }
        }

        stage('2. Build Docker Image') {
            steps {
                echo 'Собираем Production Docker-образ...'
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('3. Push to DockerHub via Vault') {
            steps {
                echo 'Забираем пароль из Vault и отправляем образ...'
                withVault(
                    vaultUrl: 'http://localhost:8200', 
                    vaultSecrets: [[
                        path: 'secret/data/dockerhub-creds',
                        engineVersion: 2, 
                        secretValues: [[envVar: 'DOCKER_PASSWORD', vaultKey: 'password']]
                    ]]
                ) {
                    // Используем переменную, полученную из Vault
                    sh "echo ${DOCKER_PASSWORD} | docker login -u ainurgilm --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }
    }
    
    post {
        success {
            echo '🎉 Пайплайн успешно завершен! Образ в DockerHub обновлен.'
        }
        failure {
            echo '❌ Сборка упала. Проверьте логи.'
        }
    }
}