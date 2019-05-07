#!/bin/bash

#export ipRomario=$(kubectl get pods -o wide | grep romario | awk '{ print $6 }')
echo " "
echo Evaluating:
echo curl -X POST -F file=@$1 http://localhost:30966/test_run_pipeline
echo " "
echo Requires tunneling through 30966:<k8s-kf-node-name>:30966
echo " "
curl -X POST -F file=@$1 http://localhost:30966/test_run_pipeline
