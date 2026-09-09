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

        stage('Airflow DAG Validation') {
            steps {
                sh '''
                    python3 - <<'PY'
                    import sys
                    import pathlib
                    import py_compile

                    dag_dir = pathlib.Path("airflow/dags")

                    for file in dag_dir.glob("*.py"):
                        print(f"Validating {file}")
                        py_compile.compile(str(file), doraise=True)

                    print("Airflow DAG syntax validation passed")
                    PY
                '''
            }
        }

        stage('Finish') {
            steps {
                echo 'CI pipeline finished successfully'
            }
        }
    }
}