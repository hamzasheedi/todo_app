---
name: deployment-coordinator
description: Coordinate frontend and backend deployment with proper environment configuration, secrets management, CI/CD integration, and independent deployment capabilities
---

# Deployment Coordinator Skill

## Purpose

This skill should be used when coordinating frontend and backend deployment with proper environment configuration, secrets management, CI/CD integration, and independent deployment capabilities for the Phase II Todo Full-Stack Web Application. The skill focuses on creating reliable, secure, and efficient deployment processes that support continuous delivery.

## When to Use This Skill

Use this skill when:
- Setting up deployment infrastructure and processes
- Configuring environment variables and secrets management
- Implementing CI/CD pipelines for automated deployment
- Coordinating frontend and backend deployments
- Managing environment-specific configurations
- Ensuring zero-downtime deployments and rollbacks

## How to Use This Skill

### Environment Configuration
1. Implement comprehensive environment variable management
2. Create environment-specific configuration files
3. Implement proper secrets management with vault or similar
4. Add configuration validation and error checking
5. Create environment-specific optimization settings
6. Implement secure configuration loading
7. Add configuration backup and recovery procedures

### CI/CD Pipeline Setup
1. Configure automated build and test pipelines
2. Implement automated deployment triggers
3. Add comprehensive testing before deployment
4. Create staging and production deployment stages
5. Implement automated rollback procedures
6. Add deployment notifications and monitoring
7. Maintain deployment audit trails

### Secrets Management
1. Implement secure secrets storage and retrieval
2. Use environment-specific secret management
3. Add secrets rotation and renewal procedures
4. Implement proper access controls for secrets
5. Create secrets backup and recovery procedures
6. Add secrets monitoring and alerting
7. Ensure compliance with security standards

### Deployment Strategies
1. Implement blue-green deployment strategy
2. Add canary deployment capabilities
3. Create zero-downtime deployment procedures
4. Implement proper health checks and monitoring
5. Add automated rollback capabilities
6. Create deployment validation procedures
7. Establish deployment scheduling and coordination

### Infrastructure Management
1. Configure containerization with Docker
2. Set up orchestration with Kubernetes or similar
3. Implement proper resource allocation and scaling
4. Add monitoring and alerting systems
5. Create backup and disaster recovery procedures
6. Implement proper logging and observability
7. Ensure infrastructure security and compliance

### Monitoring and Observability
1. Implement comprehensive application monitoring
2. Add infrastructure monitoring and alerting
3. Create performance monitoring dashboards
4. Implement error tracking and reporting
5. Add user experience monitoring
6. Create deployment success metrics
7. Establish incident response procedures

## Available Resources

### Environment Configuration
- Use `.env.example` for environment variable templates
- Reference `/docs/deployment.md` for deployment instructions
- Follow established patterns for consistency
- Include proper validation and error checking

### Deployment Scripts
- Use `/scripts/deploy.sh` for deployment automation
- Follow established patterns for consistency
- Include proper error handling and validation
- Implement comprehensive deployment procedures

### Docker Configuration
- Reference `/docker/` for containerization setup
- Follow established patterns for consistency
- Include proper security and optimization
- Implement proper multi-stage builds

### Configuration Management
- Use `/backend/.env` and `/frontend/.env` for environment configuration
- Follow established patterns for consistency
- Include proper validation and security
- Implement proper management procedures

## Output Standards

When coordinating deployments:
1. Ensure proper secrets management and security
2. Include comprehensive environment configuration
3. Implement automated CI/CD pipelines
4. Use zero-downtime deployment strategies
5. Document all deployment procedures with proper examples
6. Implement comprehensive monitoring and alerting
7. Optimize for reliability and efficiency
8. Follow deployment best practices and security standards
9. Test all deployment procedures thoroughly
10. Maintain comprehensive deployment documentation and audit trails