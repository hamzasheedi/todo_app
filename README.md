# Todo CLI Application

A command-line interface application for managing todo tasks with advanced features including priorities, tags, search, filtering, sorting, recurring tasks, and reminders.

## Features

- Add, view, update, and delete tasks
- Mark tasks as complete/incomplete
- Set task priorities (high, medium, low)
- Organize tasks with tags
- Search and filter tasks
- Sort tasks by various criteria
- Recurring tasks with different intervals
- Time-based reminders for tasks
- Backup and restore functionality
- Configuration management
- Comprehensive error handling

## Installation

### Prerequisites
- Python 3.11 or higher

### Install from source
```bash
git clone <repository-url>
cd todo-cli-app
pip install -e .
```

### Install from PyPI
```bash
pip install todo-cli-app
```

## Usage

### Interactive Mode
```bash
todo
```
This will launch the interactive menu-driven interface.

### Command Line Usage
```bash
# Add a task
todo add "Buy groceries" "Milk, bread, eggs"

# Add a task with priority and tags
todo add "Important meeting" --priority high --tags work,urgent

# View all tasks
todo list

# View tasks with specific status
todo list --status incomplete

# View tasks with specific priority
todo list --priority high

# Filter tasks by tag
todo list --tag work

# Search tasks
todo search "groceries"

# Update a task
todo update <task-id> --title "New title" --description "New description"

# Mark a task as complete
todo complete <task-id>

# Mark a task as incomplete
todo incomplete <task-id>

# Delete a task
todo delete <task-id>

# Sort tasks
todo list --sort priority

# Add a recurring task
todo recurring add "Daily exercise" --interval daily --start-date 2025-01-01

# Add a reminder
todo reminder add <task-id> --time "2025-01-02T09:00:00"
```

## Configuration

The application stores configuration in `~/.todo/config.json`:
```json
{
  "default_priority": "medium",
  "show_completed": true,
  "auto_backup": true,
  "backup_retention_days": 30,
  "storage_path": "/home/user/.todo/tasks.json"
}
```

## Data Model

### Task Attributes
- `id`: Unique identifier (UUID string)
- `title`: Task title (1-200 characters)
- `description`: Task description (0-1000 characters)
- `status`: Completion status ("incomplete", "complete")
- `priority`: Task priority ("low", "medium", "high")
- `tags`: Array of category tags (0-10 tags)
- `due_date`: Optional deadline (ISO 8601 datetime string)
- `created_date`: Timestamp of creation (ISO 8601 datetime string)
- `updated_date`: Timestamp of last modification (ISO 8601 datetime string)
- `recurrence_pattern`: Optional recurrence rule for recurring tasks

### Recurring Task Attributes
- `base_task`: Template task with all standard task attributes
- `recurrence_rule`: Frequency pattern ("daily", "weekly", "monthly", "yearly")
- `next_occurrence`: Next scheduled occurrence (ISO 8601 datetime string)
- `is_active`: Enable/disable flag
- `end_date`: Optional end date for recurrence (ISO 8601 datetime string)
- `continue_after_completion`: Policy for continuing after completion

### Reminder Attributes
- `task_id`: Reference to associated task
- `reminder_time`: Scheduled notification time (ISO 8601 datetime string)
- `status`: Current status ("pending", "triggered", "missed", "cancelled")

## Advanced Features

### Recurring Tasks
Create tasks that automatically generate new instances based on recurrence rules:
- Daily, weekly, monthly, or yearly intervals
- Optional end dates for recurrence
- Configurable continuation policies after task completion

### Reminders
Set time-based notifications for tasks:
- ISO 8601 datetime format required
- Multiple reminders per task
- Automatic status tracking (pending, triggered, missed)

### Search and Filter
- Search by keyword in title or description
- Filter by status, priority, or tags
- Sort by priority, due date, or alphabetically

### Backup and Restore
Automatic backup functionality:
- Configurable backup retention
- Manual backup creation
- Restore from previous backups

## Development

### Running Tests
```bash
pytest
```

### Running Specific Tests
```bash
pytest tests/test_task.py
```

### Code Quality
```bash
# Run all tests
pytest tests/

# Check code coverage
pytest --cov=src tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues, please file a bug report in the GitHub repository.