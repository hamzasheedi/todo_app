# Quickstart Guide: Todo App Feature Progression

**Created**: 2025-12-17
**Feature**: Todo App Feature Progression - "The Evolution of Todo"

## Getting Started

### Prerequisites
- Python 3.13 or higher
- pip package manager
- Git (optional, for source installation)

### Installation

#### Option 1: Install from PyPI (Recommended)
```bash
pip install todo-cli-app
```

#### Option 2: Install from Source
```bash
git clone <repository-url>
cd todo-app
pip install -e .
```

### Initial Setup
After installation, run the application to initialize configuration:
```bash
todo --help
```

## Basic Usage

### Main Menu Navigation
The application provides an interactive menu-driven interface:

1. **Add Task**: Create a new task with title and description
   ```
   todo add "Buy groceries" "Milk, bread, eggs"
   ```

2. **View Tasks**: Display all tasks with status indicators
   ```
   todo list
   ```

3. **Update Task**: Modify existing task details
   ```
   todo update <task-id> --title "New title" --description "New description"
   ```

4. **Mark Complete/Incomplete**: Update task completion status
   ```
   todo complete <task-id>
   todo incomplete <task-id>
   ```

5. **Delete Task**: Remove a task from the system
   ```
   todo delete <task-id>
   ```

## Phase II Features (Intermediate)

### Priorities & Categories
```bash
# Add task with priority
todo add "Important meeting" --priority high

# Filter by priority
todo list --priority high

# Add tags to task
todo update <task-id> --add-tag work --add-tag urgent

# Filter by tags
todo list --tag work
```

### Search & Filter
```bash
# Search tasks by keyword
todo search "groceries"

# Filter tasks by status
todo list --status incomplete

# Sort tasks
todo list --sort priority
```

## Phase III Features (Advanced)

### Recurring Tasks
```bash
# Create recurring task
todo recurring add "Daily exercise" --interval daily --start-date 2025-01-01
```

### Reminders
```bash
# Set reminder for task
todo reminder add <task-id> --time "2025-01-02T09:00:00"
```

## Configuration

The application stores configuration in `~/.todo/config.json`:

```json
{
  "default_priority": "medium",
  "display_format": "detailed",
  "auto_backup": true,
  "backup_location": "~/Documents/todo-backups/"
}
```

## Troubleshooting

### Common Issues
1. **Command not found**: Ensure the package was installed correctly and is in your PATH
2. **Permission errors**: Check that you have write access to the configuration directory
3. **Corrupted data**: Use `todo backup restore` to restore from a previous backup

### Data Location
- Tasks are stored in: `~/.todo/tasks.json`
- Configuration is in: `~/.todo/config.json`
- Backups are stored in: `~/.todo/backups/` (by default)

## Next Steps

1. Start by adding your first task: `todo add "Get started with Todo App"`
2. Explore the interactive menu with: `todo`
3. Review available commands with: `todo --help`
4. Check out advanced features in the full documentation