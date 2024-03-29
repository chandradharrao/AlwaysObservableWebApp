helm repo add prometheus-community https://prometheus-community.github.io/helm-charts # do if not already added
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
helm repo update
helm --debug --stderrthreshold 1 upgrade --install prometheus prometheus-community/kube-prometheus-stack -n default -f alert-rules.yaml -f alertmanager-config.yaml # helps in debugging also
helm install mongo-exporter prometheus-community/prometheus-mongodb-exporter -f mongodb-values.yaml
helm repo update


# helm uninstall [RELEASE_NAME] #remove installation
# helm upgrade [RELEASE_NAME] [CHART] --install

# if proxy not working change 127.0.0.1:10249 (or) "" to 0.0.0.0:10249 in metricsBindAddress 
#kubectl edit cm kube-proxy -n kube-system #change using this
# kubectl delete pod -l k8s-app=kube-proxy -n kube-system #then use this

## use only when pod setup leads to crashloopbackoff while setting up prometheus using operator (doesn't happen in kind node)
## kubectl patch ds prometheus-prometheus-node-exporter --type "json" -p '[{"op": "remove", "path" : "/spec/template/spec/containers/0/volumeMounts/2/mountPropagation"}]'

# grafana credentials -> admin, prom-operator

# get current values of kube prometheus stack => helm get values prometheus --all > temp.yaml # where prometheus is release name
# get only user specified values => helm get values prometheus
