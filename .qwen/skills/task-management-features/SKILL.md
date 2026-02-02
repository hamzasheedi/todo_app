---
name: task-management-features
description: Implement complete task management functionality including CRUD operations, sorting capabilities, status management, and advanced features with proper user isolation
---

# Task Management Features Skill

## Purpose

This skill should be used when implementing complete task management functionality including CRUD operations, sorting capabilities, status management, and advanced features with proper user isolation for the Phase II Todo Full-Stack Web Application. The skill focuses on creating intuitive, efficient, and secure task management systems.

## When to Use This Skill

Use this skill when:
- Implementing core task CRUD operations (Create, Read, Update, Delete)
- Adding task status management and completion tracking
- Implementing sorting and filtering capabilities
- Creating advanced task features and functionality
- Ensuring proper user isolation and data security
- Optimizing task management performance

## How to Use This Skill

### Core CRUD Operations
1. Implement task creation with proper validation and user assignment
2. Create task retrieval with user isolation and filtering
3. Implement task updates with proper validation and audit trails
4. Add task deletion with proper authorization and cleanup
5. Include proper error handling and validation
6. Ensure data consistency and integrity
7. Add proper logging and monitoring

### Status Management
1. Implement task completion status toggling
2. Add status history tracking and audit trails
3. Create status change validation and business rules
4. Implement bulk status operations where appropriate
5. Add status-based filtering and search capabilities
6. Include proper validation for status transitions
7. Ensure real-time status updates across clients

### Sorting and Filtering
1. Implement multiple sorting options (Newest First, Oldest First, etc.)
2. Add advanced filtering capabilities by status, date, priority
3. Create custom view preferences and user settings
4. Implement efficient database queries for sorting/filtering
5. Add pagination for large datasets
6. Include real-time filtering and search
7. Optimize performance for large task lists

### User Isolation
1. Ensure all queries filter by authenticated user ID
2. Implement proper validation of user ownership
3. Add cross-user access prevention
4. Create proper authentication dependency injection
5. Include comprehensive validation and error handling
6. Ensure data security and privacy compliance
7. Test user isolation thoroughly

### Advanced Features
1. Implement bulk operations for multiple tasks
2. Add task import/export functionality
3. Create task categorization and tagging
4. Implement task sharing and collaboration features
5. Add task templates and recurring tasks
6. Include notification and reminder systems
7. Add advanced analytics and reporting

## Available Resources

### Backend Implementation
- Use `/backend/routes/tasks.py` for task API endpoints
- Follow established patterns for consistency
- Include proper validation and error handling
- Implement user isolation and security measures

### Frontend Components
- Reference `/frontend/components/TaskList.tsx` for task display
- Use `/frontend/components/TaskForm.tsx` for task creation/editing
- Follow established patterns for consistency
- Include proper state management and user feedback

### Filtering Utilities
- Use `/backend/utils/task_filters.py` for advanced filtering
- Implement efficient database queries
- Follow established patterns for consistency
- Include proper validation and error handling

### Database Models
- Reference `/backend/models/` for task model definitions
- Follow established patterns for consistency
- Include proper relationships and constraints
- Implement proper indexing strategies

## Output Standards

When implementing task management features:
1. Ensure all operations maintain proper user isolation and security
2. Include comprehensive validation and error handling
3. Implement efficient database queries and performance optimization
4. Use consistent UI/UX patterns across all task operations
5. Document all features with proper examples and usage
6. Implement proper audit trails and logging
7. Optimize for performance with large datasets
8. Follow security best practices and prevent data breaches
9. Test all features thoroughly including edge cases
10. Maintain data consistency and integrity across operations