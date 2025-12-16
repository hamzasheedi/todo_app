# Data Model: Todo App Feature Progression

**Created**: 2025-12-17
**Feature**: Todo App Feature Progression - "The Evolution of Todo"

## Entity Definitions

### Task
**Description**: Represents a single todo item with all its attributes and metadata

**Attributes**:
- `id`: Unique identifier (UUID string, required, immutable)
- `title`: Task title (string, required, 1-200 characters)
- `description`: Task description (string, optional, 0-1000 characters)
- `status`: Completion status (enum: "incomplete", "complete", default: "incomplete")
- `priority`: Task priority level (enum: "low", "medium", "high", default: "medium", sort order: high → medium → low)
- `tags`: Array of category tags (string array, optional, 0-10 tags)
- `due_date`: Optional deadline (ISO 8601 datetime string, optional)
- `created_date`: Timestamp of creation (ISO 8601 datetime string, required, immutable)
- `updated_date`: Timestamp of last modification (ISO 8601 datetime string, required, auto-updated)
- `recurrence_pattern`: Optional recurrence rule (string, optional, for recurring tasks)

**Validation Rules**:
- Title: 1-200 characters, not empty
- Description: 0-1000 characters
- Status: Must be "incomplete" or "complete"
- Priority: Must be "low", "medium", or "high"
- Tags: Array length 0-10, each tag max 50 characters
- Due date: Valid ISO 8601 format if provided
- Created date: Valid ISO 8601 format, immutable once set
- Updated date: Valid ISO 8601 format, updated on any change

**State Transitions**:
- `incomplete` → `complete`: When task is marked as done
- `complete` → `incomplete`: When task completion is reversed

### TaskList
**Description**: Collection of Task entities with standardized operations

**Attributes**:
- `tasks`: Array of Task objects

**Operations**:
- `add(task)`: Add a new task to the list
- `remove(id)`: Remove task by ID
- `update(id, updates)`: Update task fields by ID
- `filter(criteria)`: Filter tasks based on criteria
- `sort(comparator)`: Sort tasks based on comparator function
- `search(keyword)`: Search tasks by keyword in title/description

### Reminder
**Description**: Notification system entity for time-based alerts

**Attributes**:
- `task_id`: Reference to associated task (string, required)
- `reminder_time`: Scheduled notification time (ISO 8601 datetime string, required)
- `is_triggered`: Status flag (boolean, default: false)
- `created_date`: Timestamp of reminder creation (ISO 8601 datetime string, required)

**Validation Rules**:
- Task ID: Must reference an existing task
- Reminder time: Must be a future date/time
- Created date: Valid ISO 8601 format

**State Transitions**:
- `false` → `true`: When reminder is triggered

### RecurringTask
**Description**: Specialized task type for automated task generation

**Attributes**:
- `base_task`: Template task (Task object, required)
- `recurrence_rule`: Frequency pattern (string, required: "daily", "weekly", "monthly", "yearly")
- `next_occurrence`: Next scheduled occurrence (ISO 8601 datetime string, required)
- `is_active`: Enable/disable flag (boolean, default: true)
- `end_date`: Optional end date for recurrence (ISO 8601 datetime string, optional)
- `continue_after_completion`: Policy for continuing recurrence after task completion (enum: "always_continue", "prompt_user", "stop_if_completed", default: "always_continue")

**Validation Rules**:
- Base task: Valid Task object with required fields
- Recurrence rule: Must be one of allowed values
- Next occurrence: Must be a future date/time
- End date: Must be after next occurrence if provided

**State Transitions**:
- `active` → `inactive`: When recurrence is disabled
- `inactive` → `active`: When recurrence is re-enabled

## Relationships

### Task to Reminder
- One-to-Many: One Task can have multiple Reminders
- Bidirectional: Reminder references Task by ID, Task may have associated reminders

### Task to RecurringTask
- One-to-Many: One base Task can generate multiple RecurringTask instances
- Unidirectional: RecurringTask references base Task

## Storage Schema

### JSON Structure
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "string",
      "description": "string",
      "status": "incomplete|complete",
      "priority": "low|medium|high",
      "tags": ["string"],
      "due_date": "ISO8601-datetime-string",
      "created_date": "ISO8601-datetime-string",
      "updated_date": "ISO8601-datetime-string",
      "recurrence_pattern": "string"
    }
  ],
  "reminders": [
    {
      "task_id": "uuid-string",
      "reminder_time": "ISO8601-datetime-string",
      "is_triggered": boolean,
      "created_date": "ISO8601-datetime-string"
    }
  ],
  "recurring_tasks": [
    {
      "base_task": { /* Task object */ },
      "recurrence_rule": "daily|weekly|monthly|yearly",
      "next_occurrence": "ISO8601-datetime-string",
      "is_active": boolean,
      "end_date": "ISO8601-datetime-string",
      "continue_after_completion": "always_continue|prompt_user|stop_if_completed"
    }
  ]
}
```

## Validation Rules Summary

### Business Rules
1. Task titles must be 1-200 characters
2. Task descriptions must be 0-1000 characters
3. Task priorities must be one of: "low", "medium", "high"
4. Tasks can have 0-10 tags maximum
5. Due dates must follow ISO 8601 format when present
6. Created dates are immutable after creation
7. Updated dates are automatically set when any field changes
8. Reminder times must be in the future
9. Recurring tasks must have valid recurrence rules
10. Recurring task next occurrences must be in the future