import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import Dashboard from '../components/Dashboard';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/v1/customers/', (req, res, ctx) => {
    return res(ctx.json(['Customer A', 'Customer B']));
  }),
  rest.get('/api/v1/sales-data/', (req, res, ctx) => {
    return res(ctx.json({ data: [] }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('renders Dashboard component', async () => {
  const queryClient = new QueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );

  expect(screen.getByText(/Loading/i)).toBeInTheDocument();

  await waitFor(() => expect(screen.getByLabelText(/Customers/i)).toBeInTheDocument());
});
