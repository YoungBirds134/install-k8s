pipeline {
  agent {
    label 'agent-13'
  }
  environment {
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
              [name: '*/develop']
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
                }          }
        }
      }
    }

    // ... other stages ...
  }

<!-- https://devopscube.com/declarative-pipeline-parameters/ -->

<!-- Note: The parameters specified in the Jenkinsfile will appear in the job only after the first run. Your first job run will fail as you will not be able to provide the parameter value through the job. -->