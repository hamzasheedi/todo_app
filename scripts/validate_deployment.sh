#!/bin/bash
# Script to validate deployment status

echo "Validating deployment status..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "Minikube is not running"
    exit 1
fi

# List pods
echo "Current pods:"
kubectl get pods

# List services
echo "Current services:"
kubectl get svc

echo "Validation complete."