#!/bin/bash

export ipRomario=$(kubectl get pods -o wide | grep romario | awk '{ print $6 }')

curl -X POST -F file=@$1 http://${ipRomario}:6966/test_run_pipeline
