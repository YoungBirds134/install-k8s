helm repo add sonarqube https://SonarSource.github.io/helm-chart-sonarqube
helm show values sonarqube/sonarqube > values.yaml
helm install my-sonarqube sonarqube/sonarqube -f values.yaml

helm uninstall sonarqube



https://stackoverflow.com/questions/63283477/helm-postgres-cannot-create-directory