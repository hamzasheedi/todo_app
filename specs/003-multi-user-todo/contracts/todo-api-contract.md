# API Contract: Phase II Multi-User Todo Application

## Overview

This document defines the API contract for the Phase II Multi-User Todo Application. All endpoints require JWT authentication and enforce user isolation by validating that the user_id in the URL matches the authenticated user's identity.

## Authentication

All API endpoints (except authentication endpoints) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly error message",
    "details": "Optional technical details"
  }
}
```

## Endpoints

### Authentication (Better Auth)

#### User Registration
- **Endpoint**: `POST /api/auth/signup`
- **Description**: Create a new user account
- **Request**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure-password"
  }
  ```
- **Response**:
  - `200`: User created successfully
  - `400`: Validation error
  - `409`: Email already exists

#### User Login
- **Endpoint**: `POST /api/auth/signin`
- **Description**: Authenticate user and return JWT token
- **Request**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure-password"
  }
  ```
- **Response**:
  - `200`: Authentication successful
  - `400`: Invalid credentials
  - `401`: Authentication failed

#### User Logout
- **Endpoint**: `POST /api/auth/signout`
- **Description**: Invalidate user session
- **Response**:
  - `200`: Logout successful

### Task Management

#### Get User's Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Description**: Retrieve all tasks for the specified user
- **Parameters**:
  - `user_id`: User's UUID (must match authenticated user)
  - `sort`: Optional sort order ("newest_first", "oldest_first", "highest_priority", "lowest_priority")
  - `status`: Optional filter by status ("all", "complete", "incomplete")
- **Headers**: Authorization: Bearer <token>
- **Response**:
  - `200`: Tasks retrieved successfully
    ```json
    {
      "success": true,
      "data": {
        "tasks": [
          {
            "id": "task-uuid",
            "user_id": "user-uuid",
            "title": "Task title",
            "description": "Task description",
            "status": "incomplete",
            "created_date": "2023-12-19T10:00:00Z",
            "updated_date": "2023-12-19T10:00:00Z"
          }
        ]
      }
    }
    ```
  - `401`: Unauthorized (invalid token)
  - `403`: Forbidden (user_id doesn't match authenticated user)
  - `404`: User not found

#### Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Description**: Create a new task for the specified user
- **Parameters**:
  - `user_id`: User's UUID (must match authenticated user)
- **Headers**: Authorization: Bearer <token>
- **Request Body**:
  ```json
  {
    "title": "Task title (1-200 chars)",
    "description": "Task description (optional, 0-1000 chars)",
    "status": "incomplete"  // Optional, defaults to "incomplete"
  }
  ```
- **Response**:
  - `201`: Task created successfully
    ```json
    {
      "success": true,
      "data": {
        "id": "task-uuid",
        "user_id": "user-uuid",
        "title": "Task title",
        "description": "Task description",
        "status": "incomplete",
        "created_date": "2023-12-19T10:00:00Z",
        "updated_date": "2023-12-19T10:00:00Z"
      }
    }
    ```
  - `400`: Validation error
  - `401`: Unauthorized
  - `403`: Forbidden (user_id doesn't match authenticated user)

#### Get Specific Task
- **Endpoint**: `GET /api/{user_id}/tasks/{id}`
- **Description**: Retrieve a specific task for the user
- **Parameters**:
  - `user_id`: User's UUID (must match authenticated user)
  - `id`: Task's UUID
- **Headers**: Authorization: Bearer <token>
- **Response**:
  - `200`: Task retrieved successfully
  - `401`: Unauthorized
  - `403`: Forbidden (user_id doesn't match or task doesn't belong to user)
  - `404`: Task not found

#### Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{id}`
- **Description**: Update a specific task for the user
- **Parameters**:
  - `user_id`: User's UUID (must match authenticated user)
  - `id`: Task's UUID
- **Headers**: Authorization: Bearer <token>
- **Request Body**:
  ```json
  {
    "title": "Updated task title (1-200 chars)",
    "description": "Updated task description (optional, 0-1000 chars)",
    "status": "complete"  // Optional
  }
  ```
- **Response**:
  - `200`: Task updated successfully
  - `400`: Validation error
  - `401`: Unauthorized
  - `403`: Forbidden (user_id doesn't match or task doesn't belong to user)
  - `404`: Task not found

#### Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{id}`
- **Description**: Delete a specific task for the user
- **Parameters**:
  - `user_id`: User's UUID (must match authenticated user)
  - `id`: Task's UUID
- **Headers**: Authorization: Bearer <token>
- **Response**:
  - `200`: Task deleted successfully
  - `401`: Unauthorized
  - `403`: Forbidden (user_id doesn't match or task doesn't belong to user)
  - `404`: Task not found

#### Mark Task Complete/Incomplete
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Description**: Toggle or set the completion status of a task
- **Parameters**:
  - `user_id`: User's UUID (must match authenticated user)
  - `id`: Task's UUID
- **Headers**: Authorization: Bearer <token>
- **Request Body**:
  ```json
  {
    "status": "complete"  // Required: "complete" or "incomplete"
  }
  ```
- **Response**:
  - `200`: Task status updated successfully
  - `400`: Validation error (invalid status)
  - `401`: Unauthorized
  - `403`: Forbidden (user_id doesn't match or task doesn't belong to user)
  - `404`: Task not found

## Error Codes

- `AUTH_001`: Invalid JWT token
- `AUTH_002`: Expired JWT token
- `AUTH_003`: User not found
- `TASK_001`: Task not found
- `TASK_002`: User does not own task
- `TASK_003`: Invalid task data
- `TASK_004`: User_id in URL does not match JWT subject
- `VALIDATION_001`: Validation error
- `SERVER_001`: Internal server error

## Security Requirements

1. All endpoints (except authentication) require valid JWT token
2. User_id in URL must match authenticated user's ID from JWT
3. Users can only access their own tasks
4. Input validation on all fields
5. Proper error responses without sensitive information leakage
6. Rate limiting should be implemented at infrastructure level

## Validation Rules

### Task Creation/Update
- Title: 1-200 characters, required
- Description: 0-1000 characters, optional
- Status: Must be "incomplete" or "complete"
- user_id: Must match authenticated user

### Response Time Requirements
- All endpoints should respond within 2 seconds under normal load
- Database queries should be optimized with proper indexing
- Authentication validation should be efficient