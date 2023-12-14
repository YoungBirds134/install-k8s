---

kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: postgres-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
  labels:
    type: local
spec:
  storageClassName: postgres-storage
  claimRef:
    name: data-sonarqube-postgresql-0
    namespace: default
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  local:
    path: /data/data-sonarqube-postgresql-0
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - huynt-11

---
