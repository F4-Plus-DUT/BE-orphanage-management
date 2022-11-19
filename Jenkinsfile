pipeline {
    agent any

    environment {
        DOCKER_IMAGE = ""
    }

    stages{
        stage("Test") {
            steps {
                script {
                    try {
                        sh "mv .env-jenkins .env"
                    }
                    catch (err) {
                        echo err.getMessage()
                    }
                }
                sh "pip3 install -r requirements.txt"
                sh "pytest --disable-warnings"
            }
        }

        stage("Clear") {
            steps {
                script {
                    try {
                        sh "docker rm orp-container-test-web-1 -f"
                        sh "docker rmi orp-container-test-web -f"
                        sh 'docker rm /$(docker ps --filter status=exited -q)'
                    }
                    catch (err) {
                        echo err.getMessage()
                    }
                }
            }
        }

        stage("Build") {
            steps {
                sh "sudo docker-compose up -d"
            }
        }
    }

    post {
        success {
            echo "SUCCESSFUL"
        }
        failure {
            echo "FAILED"
        }
    }
}
