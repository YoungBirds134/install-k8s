pipeline {
    agent { label 'agent-13' }
    parameters {
        string(name: 'Branch', description: 'Input name of the Environment', defaultValue: '')
        // ... other parameter definitions ...
    }


    stages {
        stage('Set Version Number') {
            steps {
                script {
                    // Use Version Number Plugin to determine version number
                    def VERSION_NUMBER = VersionNumber (versionNumberString: '${BUILD_DATE_FORMATTED, "ddMMyyyy"}-${Branch}-${BUILDS_TODAY}')
                    echo "Version Number: ${VERSION_NUMBER}"
                    
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    if (params.Branch.equals("develop")) {
                        echo "Selected environment: ${params.Branch}"
                        checkout scmGit(branches: [[name: '*/develop']], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/my-app'), extensions: [], userRemoteConfigs: [[credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/my-app.git']])
                        sh "ls -lart ./*"

                        echo "checkout scmGit success"
                        
                        echo "Selected environment: ${env.VERSION_NUMBER}"

                    } else if (params.Branch.equals("beta")) {
                        echo "Selected environment: ${params.Branch}"
                    } else if (params.Branch.equals("main")) {
                        echo "Selected environment: ${env.VERSION_NUMBER}"
                    } else {
                        catchError {
                            error("Please input the name of the branch environment to build code")
                        }
                    }
                }
            }
        }
    }

    // ... other stages ...
}

<!-- https://devopscube.com/declarative-pipeline-parameters/ -->

<!-- Note: The parameters specified in the Jenkinsfile will appear in the job only after the first run. Your first job run will fail as you will not be able to provide the parameter value through the job. -->