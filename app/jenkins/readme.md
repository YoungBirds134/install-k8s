--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create namespace

    kubectl create namespace devops-tools

# Triển Khai

    cd kubernetes-jenkins
    kubectl apply -f serviceAccount.yaml
    kubectl create -f volume.yaml   (Nếu chỉ dùng 1 node master thì change trong file tên node master như hình 1)
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml

#Lấy password

    kubectl get pods --namespace=devops-tools
    kubectl logs </name-pod> --namespace=devops-tools
    kubectl exec -it </name-pod> cat /var/jenkins_home/secrets/initialAdminPassword -n devops-tools

#Bật Enable proxy compatibility

    Dashboard -> Manage Jenkins -> Configure Global Security
    Tìm đến CSRF Protection -> Enable




