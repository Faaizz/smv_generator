pipeline {
    agent {
        docker {image "python:3.5.1"}
    }
    environment {
        DISABLE_AUTH= "true"
    }
    stages {
        stage("test"){
            steps{
                sh "python --version"
                echo "${DISABLE_AUTH}"
            }
        }
        stage('build') {
            steps {

                sh "echo Oleku!"

                retry(5){
                    echo "Hi There!"
                }

                timeout(time: 3, unit: 'MINUTES') {
                    sh '''
                        echo "Multiline text"
                        ld -ahl
                    '''
                }
            }
        }
    }
    post {
        always{
            echo "Always echo"
        }
        success{
            echo "All stages successful"
        }
        failure{
            echo "Failed"
        }
        unstable{
            echo "Run was maked as unstable"
        }
        changed{
            echo "Pipeline state has changed. e.g. Failing to passing."
        }
    }
}