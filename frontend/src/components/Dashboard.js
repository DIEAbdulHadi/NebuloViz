import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@material-ui/core';
import SalesTrendChart from './SalesTrendChart';
import SalesForecastChart from './SalesForecastChart';
import CustomerSegmentsChart from './CustomerSegmentsChart';
import SalesHeatmap from './SalesHeatmap';
import SalesDataTable from './SalesDataTable';
import LoadingSpinner from './LoadingSpinner';
import { apiClient } from '../services/apiClient';

function Dashboard() {
  const [selectedCustomers, setSelectedCustomers] = useState([]);

  const { data: customers, isLoading: customersLoading } = useQuery(
    'customers',
    async () => {
      const response = await apiClient.get('/customers/');
      return response.data;
    }
  );

  const { data: salesData, isLoading: salesDataLoading } = useQuery(
    ['salesData', selectedCustomers],
    async () => {
      const response = await apiClient.get('/sales-data/', {
        params: { customers: selectedCustomers },
      });
      return response.data;
    },
    {
      enabled: selectedCustomers.length > 0,
    }
  );

  if (customersLoading || salesDataLoading) {
    return <LoadingSpinner />;
  }

  const handleCustomerChange = (event) => {
    setSelectedCustomers(event.target.value);
  };

  return (
    <Grid container spacing={3} style={{ padding: 24 }}>
      <Grid item xs={12}>
        <FormControl variant="outlined" fullWidth>
          <InputLabel>Customers</InputLabel>
          <Select
            multiple
            value={selectedCustomers}
            onChange={handleCustomerChange}
            label="Customers"
          >
            {customers.map((customer) => (
              <MenuItem key={customer} value={customer}>
                {customer}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <SalesTrendChart data={salesData} />
      </Grid>
      <Grid item xs={12}>
        <SalesForecastChart data={salesData} />
      </Grid>
      <Grid item xs={12}>
        <CustomerSegmentsChart data={salesData} />
      </Grid>
      <Grid item xs={12}>
        <SalesHeatmap data={salesData} />
      </Grid>
      <Grid item xs={12}>
        <SalesDataTable data={salesData} />
      </Grid>
    </Grid>
  );
}

export default Dashboard;
