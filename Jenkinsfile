pipeline {

    agent any

    stages {

        stage("Code Clone") {
            steps {
                git url: 'https://github.com/nrupalsingh-thakur/two-tier-flaskapp.git', branch: 'main'
            }
        }

        stage("Build") {
            steps {
                sh "docker build -t two-tier-flask-app ."
            }
        }

        stage("Test") {
            steps {
                echo "Developer / Tester tests likh ke dega..."
            }
        }

        stage("Push to Docker Hub") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerHubCreds',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh """
                        echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin
                        docker tag two-tier-flask-app \$DOCKER_USERNAME/two-tier-flask-app
                        docker push \$DOCKER_USERNAME/two-tier-flask-app
                    """
                }
            }
        }

        stage("Deploy") {
            steps {
                sh "docker compose up -d --build"
            }
        }
    }
}
