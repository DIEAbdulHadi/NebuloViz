import React from 'react';
import { Line } from 'react-chartjs-2';
import { useQuery } from 'react-query';
import { apiClient } from '../services/apiClient';
import LoadingSpinner from './LoadingSpinner';

function SalesTrendChart() {
  const { data, isLoading, error } = useQuery('salesTrend', async () => {
    const response = await apiClient.get('/sales/trend');
    return response.data;
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <p>Error loading sales trend data.</p>;

  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: 'Sales',
        data: data.sales,
        fill: false,
        backgroundColor: '#3f51b5',
        borderColor: '#3f51b5',
      },
    ],
  };

  return <Line data={chartData} />;
}

export default SalesTrendChart;
