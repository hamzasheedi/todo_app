// Example React component template with TypeScript interface
import { useState } from 'react'

interface ComponentProps {
  title: string
  description?: string
  className?: string
}

export default function ComponentTemplate({
  title,
  description,
  className = ''
}: ComponentProps) {
  const [isLoading, setIsLoading] = useState(false)

  return (
    <div className={`p-4 border rounded-lg ${className}`}>
      <h2 className="text-lg font-semibold">{title}</h2>
      {description && <p className="text-gray-600 mt-2">{description}</p>}
      {isLoading && <div className="animate-pulse mt-4">Loading...</div>}
    </div>
  )
}