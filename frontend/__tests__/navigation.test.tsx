import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import DashboardLayout from '../app/(dashboard)/layout';
import TasksPage from '../app/(dashboard)/tasks/page';
import ChatPage from '../app/chat/page';

// Mock the authentication hook
jest.mock('../components/AuthWrapper', () => ({
  useAuth: () => ({ user: { id: 'test-user' }, loading: false })
}));

// Mock the UserContext
jest.mock('../contexts/UserContext', () => ({
  useUser: () => ({ backendUserId: 'test-backend-user-id', loading: false })
}));

describe('Navigation Elements', () => {
  test('Dashboard layout contains chat navigation link', () => {
    render(<DashboardLayout>{<div>Test Child</div>}</DashboardLayout>);
    
    const chatLink = screen.getByRole('link', { name: /AI Chat/i });
    expect(chatLink).toBeInTheDocument();
    expect(chatLink.getAttribute('href')).toBe('/chat');
  });

  test('Tasks page contains floating chat button', () => {
    render(<TasksPage />);
    
    const chatButton = screen.getByLabelText(/Open AI Chat/i);
    expect(chatButton).toBeInTheDocument();
    expect(chatButton.getAttribute('href')).toBe('/chat');
  });

  test('Chat page contains back to tasks link', () => {
    render(<ChatPage />);
    
    const backLink = screen.getByRole('link', { name: /Back to Tasks/i });
    expect(backLink).toBeInTheDocument();
    expect(backLink.getAttribute('href')).toBe('/tasks');
  });
});