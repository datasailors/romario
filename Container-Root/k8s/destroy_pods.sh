!#/bin/bash
kubectl delete pods $(kubectl get pods | grep $1 | awk '{print $1}')
