# Data Modeling Best Practices Reference

## Entity Design Principles

### 1. Single Responsibility
- Each entity should represent one clear business concept
- Avoid combining multiple concepts in a single entity
- Focus on cohesive data that belongs together

### 2. Normalization
- Eliminate data redundancy
- Organize data to minimize update anomalies
- Balance normalization with performance needs

### 3. Consistency
- Use consistent naming conventions
- Apply uniform patterns across similar entities
- Maintain standard data types for similar fields

## Field Design Guidelines

### 1. Naming Conventions
- Use descriptive, unambiguous names
- Follow consistent casing patterns (snake_case, camelCase, etc.)
- Avoid abbreviations unless universally understood
- Use plural names for collections/arrays

### 2. Data Type Selection
- Choose the most appropriate data type for the domain
- Consider storage efficiency
- Plan for future growth requirements
- Account for cross-platform compatibility

### 3. Constraints and Validation
- Define appropriate constraints for data integrity
- Use NOT NULL for required fields
- Apply unique constraints where business logic requires
- Implement check constraints for value validation

## Relationship Design Patterns

### 1. One-to-Many Relationships
- Represent with foreign key in the "many" table
- Ensure referential integrity
- Consider indexing for performance

### 2. Many-to-Many Relationships
- Use junction/bridge tables
- Include appropriate indexes
- Consider additional attributes in the relationship

### 3. One-to-One Relationships
- Determine which entity holds the foreign key
- Consider if entities should be merged
- Ensure business logic justification

## Common Design Patterns

### 1. Audit Trail Pattern
```
created_at: DateTime (required)
created_by: String/UUID (optional)
updated_at: DateTime (required)
updated_by: String/UUID (optional)
```

### 2. Soft Delete Pattern
```
deleted_at: DateTime (nullable)
deleted_by: String/UUID (nullable)
```

### 3. Status Pattern
```
status: Enum (ACTIVE, INACTIVE, PENDING, etc.)
status_changed_at: DateTime
status_changed_by: String/UUID
```

## Extensibility Considerations

### 1. Future-Proofing
- Design for expected growth in data volume
- Plan for additional fields that might be needed
- Consider versioning for schema changes

### 2. Flexibility
- Use flexible data types where appropriate
- Consider JSON/JSONB for semi-structured data
- Plan for optional or dynamic attributes

### 3. Migration Strategy
- Design with schema evolution in mind
- Plan for backward compatibility
- Consider how to handle deprecated fields

## Performance Guidelines

### 1. Indexing Strategy
- Index foreign keys
- Index frequently queried fields
- Balance query performance with write performance
- Monitor index usage and remove unused indexes

### 2. Query Optimization
- Design with common query patterns in mind
- Consider denormalization for read-heavy systems
- Plan for efficient join patterns

## Security Considerations

### 1. Data Classification
- Identify sensitive data that requires protection
- Apply appropriate access controls
- Consider encryption requirements

### 2. Privacy by Design
- Minimize data collection to what's necessary
- Plan for data retention and deletion policies
- Consider GDPR, CCPA, and other privacy regulations