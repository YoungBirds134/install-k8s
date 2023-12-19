        sudo kubeadm reset 

        sudo rm -rf /etc/docker     && sudo mkdir /etc/docker     && sudo rm -rf /etc/docker/daemon.json     && sudo touch /etc/docker/daemon.json     && sudo chmod -R 777 /etc/docker/daemon.json     && sudo echo "{ \"exec-opts\": [ \"native.cgroupdriver=systemd\" ], \"log-driver\": \"json-file\", \"log-opts\": { \"max-size\": \"100m\" }, \"storage-driver\": \"overlay2\" }" >> /etc/docker/daemon.json     && sudo systemctl daemon-reload     && sudo systemctl restart docker     && sudo rm -rf /etc/containerd/config.toml     && sudo systemctl restart containerd

        sudo kubeadm init --ignore-preflight-errors=NumCPU,Mem --apiserver-advertise-address=192.168.1.13  --pod-network-cidr=10.244.0.0/16     && sudo rm -rf $HOME/.kube     && sudo mkdir -p $HOME/.kube     && sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config     && sudo chown $(id -u):$(id -g) $HOME/.kube/config     && sudo ufw allow 6443     && sudo ufw allow 6443/tcp     && kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

        kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.1/deploy/static/provider/cloud/deploy.yaml
        
        kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.1/cert-manager.yaml

        # see what changes would be made, returns nonzero returncode if different
        kubectl get configmap kube-proxy -n kube-system -o yaml | \
        sed -e "s/strictARP: false/strictARP: true/" | \
        kubectl diff -f - -n kube-system

        # actually apply the changes, returns nonzero returncode on errors only
        kubectl get configmap kube-proxy -n kube-system -o yaml | \
        sed -e "s/strictARP: false/strictARP: true/" | \
        kubectl apply -f - -n kube-system

        kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/config/manifests/metallb-native.yaml


        sudo chmod -R 777 /etc/kubernetes
        export KUBECONFIG=/home/huynt/.kube/config-mycluster

        * https://gitlab.com/api/v4


        *token gitlab: glpat-5gQ7VRmzDUAPTyA1sTb2
        *token sonar gitlab read api: glpat-dUQ4ZUzsWgNC1WmeXssS
        docker-hub: 

        docker login -u youngbird
        dckr_pat_def5zf3NqhecEUctxBk_0o46G74

        *token sonar: squ_f2b8b81aa830a81e810b1fc2d7ef0dd40b26eafa

        


\
           -Dsonar.projectKey=YoungBirds134_my-app_AYw67RtGyHTmhM5jm_Qu \
           -Dsonar.sources=. \
           -Dsonar.css.node=. \
           -Dsonar.host.url=http://10.102.4.83:9000 \
           -Dsonar.login=26ae211fd2b056d9f19ecdf9b41c6e95c5581237"