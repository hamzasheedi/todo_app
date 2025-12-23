// Example Next.js page template with proper metadata and error handling
import { Metadata } from 'next'
import { TaskList } from '@/components/TaskList'

export const metadata: Metadata = {
  title: 'Tasks - Todo App',
  description: 'Manage your tasks efficiently',
}

export default function TasksPage() {
  return (
    <div className="container mx-auto py-6">
      <h1 className="text-2xl font-bold mb-6">My Tasks</h1>
      <TaskList />
    </div>
  )
}