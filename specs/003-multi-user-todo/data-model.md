# Data Model: Phase II Multi-User Todo Application

## Entity Models

### User
**Description**: Represents a registered user of the system with authentication credentials

**Fields**:
- `id`: UUID (Primary Key, required, immutable)
  - Type: UUID/string
  - Constraints: Unique, auto-generated
  - Purpose: Primary identifier for user records

- `email`: User's email address (required, unique)
  - Type: String
  - Constraints: Unique, valid email format, 1-255 characters
  - Purpose: User login identifier and contact method

- `created_date`: Timestamp of account creation (required, immutable)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Auto-generated on creation
  - Purpose: Track when user account was created

- `updated_date`: Timestamp of last modification (required, auto-updated)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Auto-updated on any change
  - Purpose: Track last modification time

**Relationships**:
- One-to-Many: User → Tasks (via user_id foreign key)

### Task
**Description**: Represents a single todo item owned by a specific user

**Fields**:
- `id`: Unique identifier for the task (required, immutable)
  - Type: UUID/string
  - Constraints: Unique, auto-generated
  - Purpose: Primary identifier for task records

- `user_id`: Reference to the owning user (required, immutable)
  - Type: UUID/string (Foreign Key to User.id)
  - Constraints: Must reference existing user, immutable after creation
  - Purpose: Establish ownership and enable user isolation

- `title`: Task title (required, 1-200 characters)
  - Type: String
  - Constraints: Required, 1-200 characters
  - Purpose: Brief description of the task

- `description`: Task description (optional, 0-1000 characters)
  - Type: String
  - Constraints: Optional, 0-1000 characters
  - Purpose: Detailed information about the task

- `status`: Completion status (enum: "incomplete", "complete", default: "incomplete")
  - Type: Enum/string
  - Constraints: Must be "incomplete" or "complete", defaults to "incomplete"
  - Purpose: Track completion state of the task

- `created_date`: Timestamp of task creation (required, immutable)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Auto-generated on creation
  - Purpose: Track when task was created

- `updated_date`: Timestamp of last modification (required, auto-updated)
  - Type: DateTime (ISO 8601 format)
  - Constraints: Auto-updated on any change
  - Purpose: Track last modification time

**Relationships**:
- Many-to-One: Task → User (via user_id foreign key)

## Database Schema

### Tables

#### users
```
id: UUID PRIMARY KEY
email: VARCHAR(255) UNIQUE NOT NULL
created_date: TIMESTAMP NOT NULL
updated_date: TIMESTAMP NOT NULL
```

**Indexes**:
- Primary: id
- Unique: email
- Regular: created_date, updated_date

#### tasks
```
id: UUID PRIMARY KEY
user_id: UUID NOT NULL REFERENCES users(id)
title: VARCHAR(200) NOT NULL
description: TEXT
status: VARCHAR(20) NOT NULL DEFAULT 'incomplete'
created_date: TIMESTAMP NOT NULL
updated_date: TIMESTAMP NOT NULL
```

**Indexes**:
- Primary: id
- Foreign: user_id (with index for efficient user-based queries)
- Regular: created_date, updated_date, status

## Validation Rules

### User Validation
- Email must be unique across all users
- Email must follow valid email format
- Email length must be 1-255 characters
- All fields except updated_date are immutable after creation (except updated_date auto-update)

### Task Validation
- Title must be 1-200 characters
- Description must be 0-1000 characters
- Status must be either "incomplete" or "complete"
- user_id must reference an existing user
- user_id is immutable after creation
- All fields except updated_date are immutable after creation (except updated_date auto-update)

## Security Constraints

### Data Isolation
- All queries must filter by authenticated user's ID
- Cross-user access must be prevented at database level
- Foreign key constraint ensures referential integrity
- User_id cannot be modified after task creation

### Access Control
- Each task is owned by exactly one user
- Users can only access tasks where user_id matches their own ID
- Database queries must always include user_id filter
- No direct access to other users' tasks is possible

## State Transitions

### Task Status Transitions
- Default state: "incomplete"
- Transitions: "incomplete" ↔ "complete" (bidirectional)
- Status can be changed multiple times
- Each status change updates the updated_date field

## Indexing Strategy

### Performance Optimization
- Index on user_id for efficient user-based queries
- Index on created_date for chronological sorting
- Index on updated_date for recency-based queries
- Index on status for filtering by completion state

## Migration Considerations

### Schema Evolution
- All new fields should have appropriate default values
- Changes to existing fields should maintain backward compatibility
- Foreign key constraints must be maintained during migrations
- Data validation must be preserved during schema updates