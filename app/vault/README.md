helm repo add hashicorp https://helm.releases.hashicorp.com
helm search repo hashicorp/vault
helm show values hashicorp/vault  > values.yaml
