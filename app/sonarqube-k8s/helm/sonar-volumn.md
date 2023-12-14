kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: sonar-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: sonar-pv
  labels:
    type: local
spec:
  storageClassName: sonar-storage
  claimRef:
    name: sonarqube-sonarqube
    namespace: default
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  local:
    path: /data/sonar-pv
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - huynt-11

---