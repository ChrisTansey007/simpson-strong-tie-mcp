import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders Simpson Strong-Tie header and status cards', () => {
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );

    expect(screen.getByText('Simpson Strong-Tie Expert MCP')).toBeDefined();
    expect(screen.getByText('Admin API Status')).toBeDefined();
    expect(screen.getByText('MCP Server Foundation')).toBeDefined();
  });
});
