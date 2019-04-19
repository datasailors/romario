#!/bin/bash

watch -n 1 kubectl get pods -o wide | grep romario-deployment
