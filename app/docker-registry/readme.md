    mkdir ~/k8s-registry
    cd ~/k8s-registry
    git clone https://gitlab.com/gitlab-org/container-registry.git
    cd container-registry
    git checkout v2.13.1-gitlab
    docker build -t your_dockerhub_username/registry:dev .
    docker login
    docker push your_dockerhub_username/registry:dev
    cd ~/k8s-registry
    nano chart_values.yaml
    helm repo add twuni https://helm.twun.io
    helm repo update
    helm install docker-registry twuni/docker-registry -f chart_values.yaml

#Adding Account Authentication and Configuring Kubernetes Access

    docker run --rm -ti xmartlabs/htpasswd username password >> htpasswd_file
    nano chart_values.yaml
    helm upgrade docker-registry twuni/docker-registry -f chart_values.yaml
    docker pull registry.your_domain/mysql
    docker login registry.your_domain
    docker pull registry.your_domain/mysql
    sudo kubectl create secret docker-registry regcred --docker-server=registry.your_domain --docker-username=your_username --docker-password=your_password