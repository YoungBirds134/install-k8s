# install-k8s on ubuntu 20.4
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#docker

    sudo apt update
    && lsmod | grep br_netfilter
    && sudo modprobe br_netfilter
    && sudo sysctl net.bridge.bridge-nf-call-iptables=1
 --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
    && sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    && sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

    && apt-cache policy docker-ce
    && sudo apt install docker-ce -y
    && sudo usermod -aG docker ${USER}
    && su - ${USER}

    sudo rm -rf /etc/docker
    && sudo mkdir /etc/docker
    && sudo rm -rf /etc/docker/daemon.json
    && sudo touch /etc/docker/daemon.json
    && sudo chmod -R 777 /etc/docker/daemon.json
    && sudo echo "{ \"exec-opts\": [ \"native.cgroupdriver=systemd\" ], \"log-driver\": \"json-file\", \"log-opts\": { \"max-size\": \"100m\" }, \"storage-driver\": \"overlay2\" }" >> /etc/docker/daemon.json
    && sudo systemctl daemon-reload
    && sudo systemctl restart docker
    && sudo rm -rf /etc/containerd/config.toml
    && sudo systemctl restart containerd
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#k8s

    sudo apt install apt-transport-https curl -y
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
    && echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" >> ~/kubernetes.list
    && sudo mv ~/kubernetes.list /etc/apt/sources.list.d

    && sudo apt install kubelet -y
    && sudo apt install kubeadm -y
    && sudo apt install kubectl -y
    && sudo apt-get install -y kubernetes-cni
    && sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#swap

    sudo swapoff -a
    && sudo nano /etc/fstab
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#comment swap file

    Inside the file, comment out the swapfile line as shown in the screenshot below:

    # /etc/fstab: static file system information.
    #
    # Use 'blkid' to print the universally unique identifier for a
    # device; this may be used with UUID= as a more robust way to name devices
    # that works even if disks are added and removed. See fstab(5).
    #
    # <file system> <mount point>   <type>  <options>       <dump>  <pass>
    # / was on /dev/sda2 during installation
    UUID=b3b00a46-047d-4de5-8c39-88a19b81cdae /               ext4    errors=remount-ro 0       1
    # /boot/efi was on /dev/sda1 during installation
    UUID=71D9-7FBF  /boot/efi       vfat    umask=0077      0       1
    -> #/swapfile                                 none            swap    sw              0       0
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#init node in k8s

    sudo kubeadm init --ignore-preflight-errors=NumCPU,Mem --pod-network-cidr=10.244.0.0/16
    && sudo rm -rf $HOME/.kube
    && sudo mkdir -p $HOME/.kube
    && sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    && sudo chown $(id -u):$(id -g) $HOME/.kube/config
    && sudo ufw allow 6443
    && sudo ufw allow 6443/tcp
    && kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Sử dụng khi chỉ dùng một node master (huynt là tên node)
    kubectl taint nodes huynt node-role.kubernetes.io/control-plane-

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#install dashboard
#create tls
    sudo mkdir /home/huynt/bin/certs
    && sudo chmod -R 777 /home/huynt/bin/certs
    && sudo  openssl req -nodes -newkey rsa:2048 -keyout /home/huynt/bin/certs/dashboard.key -out /home/huynt/bin/certs/dashboard.csr -subj "/C=/ST=/L=/O=/OU=/CN=kubernetes-dashboard"
    && sudo openssl x509 -req -sha256 -days 365 -in /home/huynt/bin/certs/dashboard.csr -signkey /home/huynt/bin/certs/dashboard.key -out /home/huynt/bin/certs/dashboard.crt
    && sudo chmod -R 777 /home/huynt/bin/certs
    -------------------------------------------------
    kubectl create ns kubernetes-dashboard
    kubectl label node huynt role=kubernetes-dashboard
    kubectl create secret generic kubernetes-dashboard-certs --from-file=/home/huynt/bin/certs -n kubernetes-dashboard

#run file dashboard.yaml
    kubectl apply -f  dashboard.yaml

#create account admin
#run file admin-user.yaml
    kubectl apply -f  admin-user.yaml

#create token login web dashboard
    kubectl -n kubernetes-dashboard create token admin-user

-------------------------------------------------------------------------------------------------------------------#install ingress-nginx controller

    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.1/deploy/static/provider/cloud/deploy.yaml
    kubectl get pods --namespace=ingress-nginx
-------------------------------------------------------------------------------------------------------------------#install loadalancer

    # see what changes would be made, returns nonzero returncode if different
    kubectl get configmap kube-proxy -n kube-system -o yaml | \
    sed -e "s/strictARP: false/strictARP: true/" | \
    kubectl diff -f - -n kube-system

    # actually apply the changes, returns nonzero returncode on errors only
    kubectl get configmap kube-proxy -n kube-system -o yaml | \
    sed -e "s/strictARP: false/strictARP: true/" | \
    kubectl apply -f - -n kube-system

    kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/config/manifests/metallb-native.yaml

    #run file loadalancer.yaml
    kubectl apply -f  loadalancer.yaml
-------------------------------------------------------------------------------------------------------------------
#insert name hosts
    sudo nano /etc/hosts
    
    example: 192.168.1.11 congcu24.com

-------------------------------------------------------------------------------------------------------------------
#config ssl (https://cert-manager.io/docs/tutorials/acme/nginx-ingress/)
-------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#common k8s

    #reset Node
        sudo kubeadm reset 

    #Sử dụng khi chỉ dùng một node master (huynt là tên node)
        kubectl taint nodes huynt node-role.kubernetes.io/control-plane-

    #Cấu hình max pods của một node
        sudo nano /etc/default/kubelet

    #Tạo namespace (nginx-ingress: tên namespace) (huynt: tên node)
        kubectl create ns nginx-ingress
        && kubectl label node k8s-master role=nginx-ingress

    #Tạo token cho node worker join vào
        kubeadm token create --print-join-command

        kubeadm join
    #Triển khai file yaml
          kubectl apply -f <name-file>

    #Xoá file yaml
          kubectl delete -f <name-file>

    #Thông tin cluster
        kubectl cluster-info

    #Thông tin namespace
        kubectl get ns

    #Thông tin pod, service      
        kubectl get po,svc -A --namespace=nginx-ingress

    #Thông tin DaemonSet    
        kubectl get ds -n nginx-ingress

    #Thông tin ingress     
        kubectl get ingress -n nginx-ingress

    #Thông tin endpoints     
        kubectl get endpoints -n nginx-ingress

    #Thông tin pods     
        kubectl get pods -n nginx-ingress
                       
    #Thông tin deployment (nginx-ingress: tên namespace)
        kubectl get deployment -n nginx-ingress

    #Thông tin chi tiết ingress    
        kubectl describe ingress -n nginx-ingress

    #Thông tin chi tiết services  
        kubectl describe svc <name-service>  -n nginx-ingress

    #Thông tin deployment     
        kubectl describe deployment -n nginx-ingress

    #Thông tin logs     
        kubectl logs <service-name; pod-name,...>  -n <namespace>
    #Xem nội dung cấu hình hiện tại của kubectl
        kubectl config view

    #Thông tin các ReplicaSet
        kubectl get rs -o wide

---------------------------------------------------------------------------------------
#common
    #Xem port nào đang chạy
        sudo lsof -i -P -n | grep LISTEN
    #Cấp Quyền 
        sudo chmod -R 777 /home/worker/.kube/config-mycluster

    #Đứng ở node worker  gọi lệnh để tải file cấu hình master về worker (truyền file)
        sudo scp  master@172.16.128.134:/etc/kubernetes/admin.conf ~/.kube/config-mycluster

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------ERROR InternalError (failed calling webhook "ipaddresspoolvalidationwebhook.metallb.io") #1540 WHEN INSTALL  MetalLB---------------------------------------------------------------------------------------------------------------------------------------
       https://github.com/metallb/metallb/issues/1540
       
    Good day. I found the solution.
    So, for solve it i needed to create new cluster.
    First of all, when i use:
    kubeadm init --pod-network-cidr=10.244.0.0/16 i had an eror. That system can`t find --cri-socket. Problem fixed by adding
    --cri-socket=unix:///var/run/cri-dockerd.sock .
    When i create cluster, as explained above i had this issue. But note: connect: connection refused it means that host refuse connection. Also, it no matter with what webhook service o worked.
    
    Actually, i had two solution:
    
    Delete rule ValidatingWebhookConfiguration for metallb-webhook-configuration;
    Update failurePolicy=Ignore for rule ValidatingWebhookConfiguration for metallb-webhook-configuration.
    Second one is batter than first one, nut both of them are not solve the cause of the problem.
    So, i waste much time to find good solution, and during it killed my cluster :)
    But for recreation it, i decide to use --cri-socket=unix:///var/run/containerd/containerd.sock
    After manipulation, i tried to set up metalLb againe. And now, my problem pass.
    So, as i understood correctly this problem connect with docker and working with it IP pool. For full understanding needs find what difference between unix:///var/run/containerd/containerd.sock and unix:///var/run/cri-dockerd.sock
    PS: I`m use kubeadm version 1.24.0.
-----------------------------ERROR InternalError (failed calling webhook CertManager)------------------------------------------------------    (https://cert-manager.io/docs/installation/kubectl/)
    kubectl delete apiservice v1beta1.webhook.cert-manager.io
    kubectl delete mutatingwebhookconfigurations cert-manager-webhook
    kubectl delete validatingwebhookconfigurations cert-manager-webhook
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
----scp -r /home/huynt/bin 192.168.1.11:/home/huynt/bin/----------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
