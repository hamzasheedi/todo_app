---
name: sorting-implementation
description: Implement advanced backend and frontend sorting functionality with all required options plus custom filtering and search capabilities
---

# Sorting Implementation Skill

## Purpose

This skill should be used when implementing advanced backend and frontend sorting functionality with all required options plus custom filtering and search capabilities for the Phase II Todo Full-Stack Web Application. The skill focuses on creating efficient, user-friendly, and performant sorting and filtering systems.

## When to Use This Skill

Use this skill when:
- Implementing sorting functionality for task lists and data displays
- Creating advanced filtering and search capabilities
- Optimizing database queries for sorting operations
- Building user-friendly sorting interfaces
- Implementing custom view preferences and configurations
- Adding pagination for large datasets

## How to Use This Skill

### Backend Sorting Implementation
1. Implement database-level sorting for performance
2. Create efficient database queries with proper indexing
3. Add support for multiple sorting criteria (compound sorting)
4. Implement proper pagination for large datasets
5. Add sorting validation and security checks
6. Include proper error handling for sorting operations
7. Optimize queries with proper database indexing

### Frontend Sorting Interface
1. Create intuitive sorting control interfaces
2. Implement dropdowns and toggle controls for sorting options
3. Add visual indicators for current sorting state
4. Include proper accessibility attributes for sorting controls
5. Implement real-time sorting updates
6. Add user preference saving for sorting configurations
7. Create responsive sorting controls for all devices

### Sorting Options Implementation
1. Implement "Newest First" sorting (by created_date)
2. Create "Oldest First" sorting (by created_date)
3. Add "Highest Priority" sorting (by priority/status)
4. Implement "Lowest Priority" sorting (by priority/status)
5. Include custom sorting options as needed
6. Add multi-column sorting capabilities
7. Implement dynamic sorting criteria

### Filtering and Search
1. Implement advanced filtering capabilities
2. Add full-text search functionality
3. Create compound filtering with multiple criteria
4. Implement real-time filtering updates
5. Add search result highlighting
6. Include fuzzy search capabilities
7. Optimize search performance with proper indexing

### Performance Optimization
1. Implement database indexing for sorting fields
2. Use efficient query patterns for sorting operations
3. Add caching for frequently sorted data
4. Implement pagination to handle large datasets
5. Optimize frontend rendering for sorted lists
6. Add virtual scrolling for large lists
7. Monitor and optimize sorting performance

### User Experience
1. Provide clear visual feedback for sorting actions
2. Maintain selection state during sorting operations
3. Implement smooth transitions for sorting changes
4. Add keyboard navigation for sorting controls
5. Include proper loading states during sorting
6. Provide sorting history and quick access
7. Implement user preference persistence

## Available Resources

### Backend Sorting Implementation
- Use `/backend/routes/tasks.py` for sorting logic in API endpoints
- Reference `/backend/utils/task_filters.py` for filtering utilities
- Follow established patterns for consistency
- Include proper database optimization strategies

### Frontend Sorting Components
- Use `/frontend/components/TaskList.tsx` for sorting display
- Reference `/frontend/components/SearchFilter.tsx` for search/filter components
- Follow established patterns for consistency
- Include proper state management and user feedback

### Database Optimization
- Reference `/specs/database/` for indexing strategies
- Follow established patterns for consistency
- Include proper query optimization techniques
- Implement efficient database operations

### Frontend Components
- Use `/frontend/components/TaskItem.tsx` for individual task display
- Follow established patterns for consistency
- Include proper rendering optimization
- Implement proper accessibility attributes

## Output Standards

When implementing sorting functionality:
1. Ensure efficient database queries with proper indexing
2. Include comprehensive sorting options and filtering capabilities
3. Implement proper user interface for sorting controls
4. Use consistent patterns across all sorting implementations
5. Document all sorting features with proper examples
6. Implement proper performance optimization
7. Optimize for large datasets and responsive performance
8. Follow sorting and filtering best practices
9. Test all sorting scenarios thoroughly including edge cases
10. Maintain consistent user experience across all sorting operations