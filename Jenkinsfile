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

        stage('dbt Debug') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
                AWS_SECRET_ACCESS_KEY = credentials('SecretAccessKey')
                AWS_DEFAULT_REGION = 'us-east-1'
            }

            steps {
                dir('dbt') {
                    sh '''
                        dbt debug --profiles-dir .
                    '''
                }
            }
        }

        stage('Development Validation') {
            when {
                branch 'development'
            }
            steps {
                echo 'Running development branch validations'
            }
        }

        stage('Main Validation') {
            when {
                branch 'main'
            }
            steps {
                echo 'Running main branch validations'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline finished successfully'
        }

        failure {
            echo 'CI pipeline failed'
        }
    }
}