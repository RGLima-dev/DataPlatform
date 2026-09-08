pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

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

        stage('Finish') {
            steps {
                echo 'CI pipeline finished successfully'
            }
        }
    }
}