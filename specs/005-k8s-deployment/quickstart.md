# Quickstart Guide: Cloud Native Todo Chatbot Deployment

## Prerequisites

1. **Docker Desktop** with Gordon (Docker AI) enabled
   - Download Docker Desktop 4.53+ from Docker website
   - Enable Docker AI (Gordon) in Settings > Beta features
   - Sign in with your Docker account

2. **Minikube**
   - Download and install from https://minikube.sigs.k8s.io/docs/start/
   - Verify installation: `minikube version`

3. **kubectl-ai plugin**
   - Install kubectl-ai: `brew install kubectl-ai` (Mac) or `choco install kubectl-ai` (Windows)
   - Verify installation: `kubectl-ai --help`

4. **Kagent** (for health checks)
   - Install Kagent according to your platform requirements

## Setup Steps

1. **Start Minikube Cluster**
   ```bash
   minikube start
   ```

2. **Verify Cluster Status**
   ```bash
   kubectl get nodes
   ```

3. **Navigate to Project Directory**
   ```bash
   cd /path/to/todo_app
   ```

4. **Containerize Applications with Gordon**
   ```bash
   # Containerize frontend
   docker ai "Containerize my frontend application"
   
   # Containerize backend
   docker ai "Containerize my backend application"
   ```

5. **Deploy to Minikube using kubectl-ai**
   ```bash
   # Deploy frontend and backend with 2 replicas each
   kubectl-ai "Deploy frontend and backend with 2 replicas each using the Docker images I created"
   ```

6. **Expose Services**
   ```bash
   # Expose services via NodePort
   kubectl-ai "Expose frontend and backend services via NodePort"
   ```

7. **Generate Helm Chart**
   ```bash
   # Generate a Helm chart for the Todo app
   kubectl-ai "Generate a Helm chart for my Todo app"
   ```

8. **Validate Deployment with Kagent**
   ```bash
   # Analyze cluster health
   kagent "Analyze cluster health"
   ```

## Verification

1. **Check Pods Status**
   ```bash
   kubectl get pods
   ```

2. **Check Services**
   ```bash
   kubectl get svc
   ```

3. **Access the Application**
   ```bash
   minikube service [frontend-service-name] --url
   ```

## Troubleshooting

- If Docker AI (Gordon) is unavailable in your region, use standard Docker CLI commands or ask Claude Code to generate the docker run commands for you.
- If kubectl-ai commands fail, ensure your Minikube cluster is running and kubectl is properly configured.
- For deployment issues, run `kagent "analyze cluster health"` to identify problems.