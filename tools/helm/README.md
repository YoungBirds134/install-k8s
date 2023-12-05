sudo helm lint ./
sudo helm template my-app ./


sudo helm install my-ap ./~/bin/helm/myapp (đường dẫn tới chart)


sudo helm upgrade my-app ./~/bin/helm/myapp  -f values.yaml


--release (mỗi lần release phải repo index lại )

sudo helm package ./~/bin/helm/myapp  -d  ./~/bin/helm/publish


--github

sudo helm repo index ./


--tạo github đẩy lên 