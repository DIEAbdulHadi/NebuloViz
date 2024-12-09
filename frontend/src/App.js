import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { AppBar, Toolbar, Typography, ThemeProvider } from '@material-ui/core';
import ErrorBoundary from './components/ErrorBoundary';
import LoadingSpinner from './components/LoadingSpinner';
import NotFound from './components/NotFound';
import theme from './theme';

const Dashboard = lazy(() => import('./components/Dashboard'));

function App() {
  return (
    <ThemeProvider theme={theme}>
      <ErrorBoundary>
        <Router>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6">
                NebuloViz Advanced Sales Dashboard
              </Typography>
            </Toolbar>
          </AppBar>
          <Suspense fallback={<LoadingSpinner />}>
            <Switch>
              <Route exact path="/" component={Dashboard} />
              <Route component={NotFound} />
            </Switch>
          </Suspense>
        </Router>
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;
