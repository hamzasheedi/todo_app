---
name: database-specialist
description: Implement Neon PostgreSQL database schema with proper relationships, indexing, and query optimization following ACID principles
---

# Database Specialist Skill

## Purpose

This skill should be used when implementing Neon PostgreSQL database schema with proper relationships, indexing, and query optimization for the Phase II Todo Full-Stack Web Application. The skill focuses on creating robust, scalable, and performant database solutions following ACID principles and best practices.

## When to Use This Skill

Use this skill when:
- Designing database schemas based on functional requirements
- Creating SQLModel models with proper relationships
- Optimizing database queries for performance
- Implementing proper indexing strategies
- Handling database migrations and schema evolution
- Ensuring data integrity and security

## How to Use This Skill

### Database Schema Design Process
1. Analyze functional requirements to identify entities and relationships
2. Create SQLModel models with proper data types and constraints
3. Define UUID primary keys and foreign key relationships
4. Implement proper indexing strategies for efficient queries
5. Add created_date, updated_date, and audit fields as needed
6. Create migration scripts for schema changes

### Performance Optimization
1. Implement proper indexing for frequently queried fields
2. Optimize queries with proper JOIN strategies
3. Use database connection pooling for efficiency
4. Implement proper pagination for large datasets
5. Use query optimization techniques like EXPLAIN ANALYZE
6. Monitor and optimize slow queries

### Data Integrity and Security
1. Implement proper foreign key constraints with cascading rules
2. Use UUID primary keys for security and distributed systems
3. Implement proper user isolation with foreign key relationships
4. Add proper constraints to prevent data corruption
5. Implement audit trails for important operations
6. Use parameterized queries to prevent SQL injection

### Migration Management
1. Create automated migration scripts for schema changes
2. Implement proper rollback strategies
3. Test migrations in staging environment before production
4. Implement data seeding for initial data
5. Handle migration conflicts and errors gracefully
6. Document migration procedures and best practices

## Available Resources

### Database Models
- Use models in `/backend/models/` for creating new SQLModel schemas
- Follow established patterns for user ownership and relationships
- Include proper validation and constraints
- Implement proper indexing strategies

### Migration Scripts
- Use `/backend/database/migrations.py` for migration templates
- Follow established patterns for consistency
- Include proper error handling and rollback procedures
- Test migrations thoroughly before deployment

### Database Utilities
- Reference `/backend/database/` for connection and session management
- Use established patterns for connection pooling
- Implement proper session management
- Follow security best practices

### Performance Tools
- Use `/backend/database/utils.py` for query optimization utilities
- Implement proper monitoring and logging
- Follow performance optimization guidelines
- Monitor database performance metrics

## Output Standards

When implementing database solutions:
1. Ensure all schemas follow ACID principles and data integrity
2. Include proper indexing for efficient queries
3. Implement user isolation with foreign key relationships
4. Use SQLModel for database operations with proper relationships
5. Document all database schemas with proper examples
6. Implement proper migration procedures and rollback strategies
7. Optimize for performance and scalability
8. Follow security best practices and prevent common vulnerabilities
9. Implement proper audit trails and logging
10. Test migrations thoroughly before production deployment