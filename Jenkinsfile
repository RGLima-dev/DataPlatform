pipeline {
    agent any

    stages {
        stage('Inspect') {
            steps {
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Python Syntax') {
            steps {
                sh 'python3 -m compileall spark airflow/dags'
            }
        }

        stage('Tests') {
            steps {
                sh 'pytest -q'
            }
        }

        stage('Docker Compose Validation') {
            steps {
                sh 'docker compose config'
            }
        }

        stage('Finish') {
            steps {
                echo 'CI pipeline finished successfully'
            }
        }
    }
}