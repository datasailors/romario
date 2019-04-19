#!/bin/sh

# Container startup script
echo -e "\n"
echo "---------"
echo -e "\n"
echo "Notebook Token: Welcome"
echo -e "\n\n"
# Run command
jupyter notebook --allow-root --ip=0.0.0.0 --no-browser --NotebookApp.token='Welcome'

# Startup on Pipeline running
#python /service/romario.py
