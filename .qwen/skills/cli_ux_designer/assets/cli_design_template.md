# CLI UX Design Specification Template

## 1️⃣ CLI Command Structure

### Base Command
```
app-name <command> [options]
```

### Command Hierarchy
```
app-name
├── command-1
│   ├── subcommand-a
│   └── subcommand-b
├── command-2
│   └── [options]
└── help
```

---

## 2️⃣ Commands & Arguments

### Command: `command-name`
- **Description:** [Clear, concise description of what the command does]
- **Usage:** `app-name command-name [arguments] [options]`
- **Required Arguments:**
  - `argument-name`: [Description and expected format]
- **Optional Flags:**
  - `--flag-name, -f`: [Description and default value if applicable]
  - `--another-flag, -a`: [Description and default value if applicable]
- **Example Usage:**
  ```bash
  app-name command-name required-arg --flag-name value
  ```

---

## 3️⃣ Help & Discoverability

### Global Help Output (`--help` or `-h`)
```
App Name - [Brief description of the application]

Usage: app-name <command> [options]

Commands:
  command-1    [Description of command-1]
  command-2    [Description of command-2]
  help         Show help for a command

Options:
  -h, --help     Show help for a command
  -v, --version  Show version number

For more information on a specific command, run: app-name <command> --help
```

### Command-Level Help (`command-name --help`)
```
Description of what the command does

Usage: app-name command-name [arguments] [options]

Arguments:
  required-arg    [Description and expected format]

Options:
  -f, --flag-name     [Description and default value]
  -a, --another-flag  [Description and default value]
  -h, --help          Show help for this command
```

### Error Hints for Incorrect Usage
- **Unknown command:** "Command 'xyz' not found. See 'app-name --help' for available commands."
- **Missing required argument:** "Missing required argument 'arg-name'. See 'app-name command-name --help'."
- **Invalid flag:** "Invalid flag '--invalid'. See 'app-name command-name --help'."

---

## 4️⃣ Output Formatting Rules

### Lists
```
Item 1 - [Description]
Item 2 - [Description]
Item 3 - [Description]

[Total: 3 items]
```

### Single Items
```
Name: [Item Name]
Status: [Status Value]
Created: [Date/Time]
```

### Status Indicators
- Success: ✅ `[Success message]`
- Error: ❌ `[Error message]`
- Warning: ⚠️ `[Warning message]`
- In Progress: ⏳ `[Progress message]`

### Empty Results
```
No items found.
Run 'app-name command-name --help' for usage information.
```

### Formatting Conventions
- Use consistent indentation (2 spaces)
- Align similar information in columns where appropriate
- Use clear, readable typography
- Maintain consistent symbol usage

---

## 5️⃣ Error Message UX Guidelines

### Tone
- Clear and direct
- Neutral and professional
- Actionable and helpful
- Avoid technical jargon when possible

### Structure
```
Error: [Brief description of what went wrong]

[More detailed explanation if needed]

[Specific suggestion for resolution]

[Relevant command to try or check]
```

### Consistency Rules
- Always start with "Error:" for error messages
- Use consistent formatting across all commands
- Include relevant command suggestions
- Provide clear next steps when possible

---

## 6️⃣ UX Principles Applied

### Discoverability
- Commands are intuitive and predictable
- Help is easily accessible via `--help`
- Common actions are simple to find
- Error messages guide users to solutions

### Consistency
- Uniform argument patterns across commands
- Consistent help text structure
- Standardized output formatting
- Predictable error message format

### Efficiency
- Minimize typing for common operations
- Provide useful shortcuts and aliases
- Allow for power user workflows
- Reduce cognitive load through familiarity

---

*CLI design created using the cli_ux_designer skill*