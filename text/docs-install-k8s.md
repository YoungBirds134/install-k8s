# Docker Installation
sudo apt update && lsmod | grep br_netfilter && sudo modprobe br_netfilter && sudo sysctl net.bridge.bridge-nf-call-iptables=1
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo usermod -aG docker ${USER}
su - ${USER}
sudo rm -rf /etc/docker && sudo mkdir /etc/docker && sudo rm -rf /etc/docker/daemon.json && sudo touch /etc/docker/daemon.json && sudo chmod -R 777 /etc/docker/daemon.json
sudo echo "{ \"exec-opts\": [ \"native.cgroupdriver=systemd\" ], \"log-driver\": \"json-file\", \"log-opts\": { \"max-size\": \"100m\" }, \"storage-driver\": \"overlay2\" }" >> /etc/docker/daemon.json
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo rm -rf /etc/containerd/config.toml
sudo systemctl restart containerd

# Kubernetes Installation
sudo apt install apt-transport-https curl -y
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" >> ~/kubernetes.list
sudo mv ~/kubernetes.list /etc/apt/sources.list.d
sudo apt install kubelet kubeadm kubectl kubernetes-cni -y

# Disable Swap
sudo swapoff -a
sudo nano /etc/fstab # Comment out the swap entry

# Initialize Kubernetes Master Node
sudo kubeadm init --ignore-preflight-errors=NumCPU,Mem --apiserver-advertise-address=192.168.1.13 --pod-network-cidr=10.244.0.0/16
sudo rm -rf $HOME/.kube
sudo mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
sudo ufw allow 6443
sudo ufw allow 6443/tcp
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

# Ingress-Nginx Controller Installation
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.1/deploy/static/provider/cloud/deploy.yaml

# MetalLB Installation
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/manifests/namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/manifests/metallb.yaml
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/manifests/layer2-config.yaml
kubectl apply -f loadbalancer.yaml # Create and apply your loadbalancer.yaml file
                --------------------------
                apiVersion: metallb.io/v1beta1
                kind: IPAddressPool
                metadata:
                name: production
                namespace: metallb-system
                spec:
                addresses:
                - 192.168.1.11-192.168.1.11 #IP HOST dùng ingress controller
                autoAssign: true
                ---
                apiVersion: metallb.io/v1beta1
                kind: L2Advertisement
                metadata:
                name: l2-advert
                namespace: metallb-system
                spec:
                ipAddressPools:
                - default

                -------------------------
# Cert-Manager Installation
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.1/cert-manager.yaml
