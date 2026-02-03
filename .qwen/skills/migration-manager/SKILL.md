---
name: migration-manager
description: Handle comprehensive database migrations, schema evolution, data integrity, and zero-downtime migration strategies
---

# Migration Manager Skill

## Purpose

This skill should be used when handling comprehensive database migrations, schema evolution, data integrity, and zero-downtime migration strategies for the Phase II Todo Full-Stack Web Application. The skill focuses on creating safe, reliable, and efficient database migration processes.

## When to Use This Skill

Use this skill when:
- Creating database migration scripts and procedures
- Implementing schema evolution and changes
- Ensuring data integrity during migrations
- Planning zero-downtime migration strategies
- Managing database versioning and rollbacks
- Handling data migration and transformation

## How to Use This Skill

### Migration Planning
1. Analyze schema changes and dependencies
2. Plan migration sequence and dependencies
3. Create rollback procedures for each migration
4. Identify potential data transformation needs
5. Plan for zero-downtime migration strategies
6. Create migration testing procedures
7. Document migration requirements and constraints

### Migration Implementation
1. Create automated migration scripts with proper validation
2. Implement proper error handling and rollback mechanisms
3. Add comprehensive logging and monitoring
4. Include data validation and integrity checks
5. Implement proper transaction management
6. Add migration progress tracking
7. Create migration audit trails

### Zero-Downtime Strategies
1. Implement blue-green deployment for database changes
2. Create shadow migration techniques where possible
3. Add gradual rollout strategies for schema changes
4. Implement backward compatibility during transitions
5. Create migration safety checks and validations
6. Add automated rollback triggers
7. Monitor application health during migrations

### Data Integrity
1. Implement comprehensive data validation
2. Create data consistency checks
3. Add referential integrity validation
4. Include business rule validation
5. Implement data backup procedures
6. Add data recovery mechanisms
7. Create data audit and verification

### Migration Testing
1. Test migrations in staging environment first
2. Validate data integrity after migrations
3. Test rollback procedures thoroughly
4. Implement performance testing for migrations
5. Create migration automation testing
6. Add data validation testing
7. Document migration test results

### Migration Monitoring
1. Implement comprehensive migration monitoring
2. Add migration progress tracking
3. Create migration alerting systems
4. Monitor application performance during migrations
5. Track migration success and failure rates
6. Implement migration audit logging
7. Create migration reporting and dashboards

## Available Resources

### Migration Scripts
- Use `/backend/database/migrations.py` for migration templates
- Follow established patterns for consistency
- Include proper error handling and rollback procedures
- Implement comprehensive validation procedures

### Database Models
- Reference `/backend/models/` for SQLModel entity definitions
- Follow established patterns for consistency
- Include proper validation and constraints
- Implement proper relationships and indexing

### Migration Utilities
- Use `/backend/database/` for migration utilities
- Follow established patterns for consistency
- Include proper validation and error handling
- Implement comprehensive migration procedures

### Database Seeding
- Reference `/backend/database/seed.py` for data seeding
- Follow established patterns for consistency
- Include proper validation and error handling
- Implement comprehensive seeding procedures

## Output Standards

When implementing database migrations:
1. Ensure comprehensive migration planning and testing
2. Include proper rollback procedures and safety measures
3. Implement zero-downtime migration strategies where possible
4. Use consistent patterns across all migration implementations
5. Document all migration procedures with proper examples
6. Implement proper monitoring and alerting
7. Optimize for data integrity and application availability
8. Follow database migration best practices and security standards
9. Test all migration scenarios thoroughly including rollbacks
10. Maintain comprehensive migration documentation and audit trails