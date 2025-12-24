# Data Model: Todo AI Chatbot – Phase III

## Entity: Task
**Purpose**: Represents a user's to-do item with title, description, completion status, and creation timestamp

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the task
- `title` (String): Title of the task (required, max 200 characters)
- `description` (String): Detailed description of the task (optional, max 500 characters)
- `completed` (Boolean): Status indicating if task is completed (default: false)
- `created_at` (DateTime): Timestamp when task was created (auto-generated)
- `updated_at` (DateTime): Timestamp when task was last updated (auto-generated)
- `user_id` (UUID/String): Foreign key linking to user (required for multi-user isolation)

**Validation Rules**:
- Title must not be empty
- Title must be less than 200 characters
- User must be authenticated to create/access tasks

## Entity: Conversation
**Purpose**: Represents a user's interaction session with message history and context

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the conversation
- `title` (String): Title of the conversation (auto-generated from first message or user-provided)
- `created_at` (DateTime): Timestamp when conversation was started (auto-generated)
- `updated_at` (DateTime): Timestamp when conversation was last updated (auto-generated)
- `user_id` (UUID/String): Foreign key linking to user (required for multi-user isolation)

**Validation Rules**:
- User must be authenticated to create/access conversations
- Each conversation belongs to exactly one user

## Entity: Message
**Purpose**: Represents individual exchanges between user and chatbot with timestamp and content

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier for the message
- `content` (String): Content of the message (required, max 500 characters as per FR-018)
- `role` (String): Role of the message sender (either 'user' or 'assistant', required)
- `timestamp` (DateTime): When the message was sent (auto-generated)
- `conversation_id` (UUID/Integer): Foreign key linking to conversation (required)
- `user_id` (UUID/String): Foreign key linking to user (required for multi-user isolation)

**Validation Rules**:
- Content must not be empty
- Content must be less than 500 characters
- Role must be either 'user' or 'assistant'
- Each message belongs to exactly one conversation

## Entity: User
**Purpose**: Represents an authenticated individual with associated tasks and conversations

**Fields**:
- `id` (UUID/String): Primary key, unique identifier for the user
- `email` (String): User's email address (required, unique)
- `created_at` (DateTime): Timestamp when user account was created (auto-generated)
- `updated_at` (DateTime): Timestamp when user account was last updated (auto-generated)

**Validation Rules**:
- Email must be valid and unique
- User must be authenticated to access any data

## Relationships
- User (1) → Task (Many): One user can have many tasks
- User (1) → Conversation (Many): One user can have many conversations
- Conversation (1) → Message (Many): One conversation can have many messages
- User (1) → Message (Many): One user can be associated with many messages

## State Transitions
- Task: `completed: false` → `completed: true` (via complete_task MCP tool)
- Task: `completed: true` → `completed: false` (via update_task MCP tool to uncomplete)
- Message: Immutable after creation (no state transitions)
- Conversation: Updated timestamp changes on new message (via updated_at field)