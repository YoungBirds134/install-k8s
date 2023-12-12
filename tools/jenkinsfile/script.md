import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec
import net.sf.json.groovy.JsonSlurper

pipeline {
  agent {
    label 'agent-13'
  }
  tools {
    nodejs 'Node16'
  }

  environment {
    SONARQUBE_SECRET = '0d65dc703a789bcad5f4e59c851a8d2a3b105a61'
    SONARQUBE_URL = "http://10.102.4.83:9000" // Set your SonarQube URL here
    SONARQUBE_TOKEN_NAME = "0d65dc703a789bcad5f4e59c851a8d2a3b105a61" // Set your desired token name here
    DOCKERHUB_CREDENTIALS = credentials('docker_hub')

  }

  parameters {
    string(name: 'Branch', description: 'Input name of the Environment', defaultValue: '')
    // ... other parameter definitions ...
  }

  stages {

    stage('Clear Workspace') {
      steps {
        script {
          // Delete the workspace to clear it
          deleteDir()
        }
      }
    }

    stage('Check out') {
      steps {
        script {
          if (params.Branch.equals("develop")) {
            echo "Selected environment: ${params.Branch}"
            checkout scmGit(branches: [
              [name: '*/${Branch}']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/$JOB_NAME'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: '$JOB_NAME']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/$JOB_NAME.git']
            ])
            checkout scmGit(branches: [
              [name: '*/main']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/$JOB_NAME-${Branch}-config.git'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: '$JOB_NAME-${Branch}-config']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/$JOB_NAME-${Branch}-config.git']
            ])
            checkout scmGit(branches: [
              [name: '*/main']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/helm.git'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: 'helm']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/helm.git']
            ])

            sh "ls -lart ./*"

            echo "checkout scmGit success"

            echo "Selected environment: ${env.VERSION_NUMBER}"

          } else if (params.Branch.equals("beta")) {
            echo "Selected environment: ${Branch}"
            echo "Selected environment: ${Branch}"
            checkout scmGit(branches: [
              [name: '*/${Branch}']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/$JOB_NAME'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: '$JOB_NAME']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/$JOB_NAME.git']
            ])
            checkout scmGit(branches: [
              [name: '*/main']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/$JOB_NAME-${Branch}-config.git'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: '$JOB_NAME-${Branch}-config']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/$JOB_NAME-${Branch}-config.git']
            ])
            checkout scmGit(branches: [
              [name: '*/main']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/helm.git'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: 'helm']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/helm.git']
            ])

            sh "ls -lart ./*"

            echo "checkout scmGit success"

            echo "Selected environment: ${env.VERSION_NUMBER}"
          } else if (params.Branch.equals("main")) {
            echo "Selected environment: ${Branch}"
            checkout scmGit(branches: [
              [name: '*/${Branch}']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/$JOB_NAME'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: '$JOB_NAME']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/$JOB_NAME.git']
            ])
            checkout scmGit(branches: [
              [name: '*/main']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/$JOB_NAME-${Branch}-config.git'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: '$JOB_NAME-${Branch}-config']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/$JOB_NAME-${Branch}-config.git']
            ])
            checkout scmGit(branches: [
              [name: '*/main']
            ], browser: gitLabBrowser('https://gitlab.com/YoungBirds134/helm.git'), extensions: [
              [$class: 'RelativeTargetDirectory', relativeTargetDir: 'helm']
            ], userRemoteConfigs: [
              [credentialsId: '40cc97dd-78de-4ffc-a1f7-f42794debc37', url: 'https://gitlab.com/YoungBirds134/helm.git']
            ])

            sh "ls -lart ./*"

            echo "checkout scmGit success"

            echo "Selected environment: ${env.VERSION_NUMBER}"
          } else {
            catchError {
              error("Please input the name of the branch environment to build code")
            }
          }
        }
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          echo "Selected environment: ${Branch}"

          def scannerHome = tool name: 'SonarQubeScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
          withSonarQubeEnv('sonarqube-container') {
            // This expands the environment variables SONAR_CONFIG_NAME, SONAR_HOST_URL, SONAR_AUTH_TOKEN that can be used by any script.
            sh """${scannerHome}/bin/sonar-scanner \
           -Dsonar.projectKey=YoungBirds134_my-app_AYxIxrbQn19x4ZIBEiVW\
           -Dsonar.sources=. \
           -Dsonar.css.node=. \
           -Dsonar.host.url=http://10.102.4.83:9000 \
           -Dsonar.login=0d65dc703a789bcad5f4e59c851a8d2a3b105a61 
             """

            println env.SONAR_HOST_URL

            sh "cat .scannerwork/report-task.txt"
            def props = readProperties file: '.scannerwork/report-task.txt'
            echo "properties=${props}"

            def sonarServerUrl = props['serverUrl']
            def ceTaskUrl = props['ceTaskUrl']
            def ceTask
            def reportFilePath = ".scannerwork/report-task.txt"
            def reportTaskFileExists = fileExists "${reportFilePath}"
            if (reportTaskFileExists) {
              echo "Found report task file"
              def taskProps = readProperties file: "${reportFilePath}"
              def authString = '0d65dc703a789bcad5f4e59c851a8d2a3b105a61'

              echo "taskId[${taskProps['ceTaskId']}]"
              while (true) {
                sleep 10
                def taskStatusResult =
                  sh(returnStdout: true,
                    script: "curl -s -X GET -u ${authString} \'${ceTaskUrl}\'")
                echo "taskStatusResult[${taskStatusResult}]"

                def analysisId = new JsonSlurper().parseText(taskStatusResult).task.analysisId

                def url = new URL(sonarServerUrl + "/api/qualitygates/project_status?analysisId=${analysisId}")
                def taskanalysisId =
                  sh(returnStdout: true,
                    script: "curl -s -X GET -u ${authString} \'${url}\'")
                echo "taskanalysisId[${taskanalysisId}]"

                def projectId = new JsonSlurper().parseText(taskStatusResult).task.componentKey

                def projectName = new JsonSlurper().parseText(taskStatusResult).task.componentName
                def sonarQubeProjectName = "${projectId}"
                echo "sonarQubeProjectName[${sonarQubeProjectName}]"
                def qualityProfileResult =
                  sh(returnStdout: true,
                    script: "curl -s -X GET -u ${authString} \'${sonarServerUrl}/api/qualityprofiles/search?project=${sonarQubeProjectName}\'")
                echo "qualityProfileResult[${qualityProfileResult}]"

                def qualityGateResult =
                  sh(returnStdout: true,
                    script: "curl -s -X GET -u ${authString} \'${sonarServerUrl}/api/qualitygates/get_by_project?project=${sonarQubeProjectName}\'")
                echo "qualityGateResult[${qualityGateResult}]"
                echo "qualityGateResult[${qualityGateResult}]"

                def taskStatus = new JsonSlurper().parseText(taskStatusResult).task.status
                echo "taskStatus[${taskStatus}]"
                // Status can be SUCCESS, ERROR, PENDING, or IN_PROGRESS. The last two indicate it's
                // not done yet.
                if (taskStatus != "IN_PROGRESS" && taskStatus != "PENDING") {
                  break;
                }
              }
            }

          }
        }
      }
    }


    stage('Build Env') {
      steps {
        script {
          // Move files from my-app-develop-config to my-app
          sh "mv $JOB_NAME-${Branch}-config/${Branch}.env $JOB_NAME/"
          sh "cd $JOB_NAME/ && mv ${Branch}.env  .env"
        }
      }
    }

        stage('Build Image') {
            steps {
                script {
                    def VERSION_NUMBER = VersionNumber(versionNumberString: '${BUILD_DATE_FORMATTED, "yyyyMMdd"}-${Branch}-${BUILDS_TODAY}')
                    def NAME_IMAGE = "$JOB_NAME-${VERSION_NUMBER}"

                    echo "NAME_IMAGE: ${NAME_IMAGE}"

                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    echo 'Login Completed'

                    sh "cd $JOB_NAME/ && docker build -t $DOCKERHUB_CREDENTIALS_USR/$JOB_NAME:${NAME_IMAGE} ."
                    sh "cd $JOB_NAME/ && docker tag $DOCKERHUB_CREDENTIALS_USR/$JOB_NAME:${NAME_IMAGE} $DOCKERHUB_CREDENTIALS_USR/$JOB_NAME:latest "
                    sh "cd $JOB_NAME/ && docker push $DOCKERHUB_CREDENTIALS_USR/$JOB_NAME:${NAME_IMAGE}"
                    sh "cd $JOB_NAME/ && docker rmi $DOCKERHUB_CREDENTIALS_USR/$JOB_NAME:${NAME_IMAGE}"
                    sh 'docker logout'

                    // Navigate to the helm/myapp directory
                    dir('helm/myapp') {
                        // Define the content to be added to values.yaml
                        def contentToAdd = 
                        """
image:
    repository: ${DOCKERHUB_CREDENTIALS_USR}/${JOB_NAME}
    tag: ${NAME_IMAGE}
    pullPolicy: Always 
                        """

                        // Use echo and heredoc to append content to values.yaml
                        sh "echo '${contentToAdd}' >> values.yaml"
                    }
                    // Check if the release exists
                    def releaseExists = sh(script: 'helm list -q | grep -w $JOB_NAME', returnStatus: true) == 0

                    // Use helm install or helm upgrade based on release existence
                    if (releaseExists) {
                        sh 'cd helm/myapp && helm upgrade $JOB_NAME . -f values.yaml'
                    } else {
                        sh 'cd helm/myapp && helm install $JOB_NAME . -f values.yaml'
          }
        }
      }
    }
  }
  
}