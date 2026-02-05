# Data Model: Cloud Native Kubernetes Deployment

## Key Entities

### Deployment Package
- **Description**: Contains all Kubernetes resources needed to deploy the Todo Chatbot application
- **Components**: 
  - Frontend Deployment
  - Backend Deployment
  - Frontend Service
  - Backend Service
  - ConfigMaps
  - Secrets
- **Relationships**: Contains multiple Kubernetes resources

### Container Images
- **Description**: Docker images for frontend and backend components created using AI-assisted tools
- **Attributes**:
  - Image Name
  - Image Tag
  - Registry Location
  - Build Context
- **Relationships**: Referenced by Deployments in Deployment Package

### Helm Chart
- **Description**: Packaged Kubernetes resources with configurable parameters for deployment
- **Components**:
  - Chart.yaml (metadata)
  - values.yaml (configuration)
  - templates/ directory (Kubernetes manifests)
  - charts/ directory (dependencies)
- **Relationships**: Packages the Deployment Package into a versionable format

### Health Reports
- **Description**: Validation results from post-deployment health checks
- **Attributes**:
  - Component Status
  - Resource Utilization
  - Connectivity Checks
  - Performance Metrics
- **Relationships**: Generated after deployment validation