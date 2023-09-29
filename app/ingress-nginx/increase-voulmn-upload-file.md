-- how is server allowed  upload volumn?

    kubectl exec -n ingress-nginx  ingress-nginx-controller-8c4c57cd9-b7vkx cat nginx.conf|grep client_max_body_size

-- edit configmap
    kubectl edit configmaps ingress-nginx-controller  -n ingress-nginx

-- add code in line: data

    proxy-body-size: 10m


