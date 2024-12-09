import React from 'react';
import { Heatmap } from 'react-chartjs-2';
import { useQuery } from 'react-query';
import { apiClient } from '../services/apiClient';
import LoadingSpinner from './LoadingSpinner';

function SalesHeatmap() {
  const { data, isLoading, error } = useQuery('salesHeatmap', async () => {
    const response = await apiClient.get('/sales/heatmap');
    return response.data;
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <p>Error loading sales heatmap.</p>;

  const chartData = {
    datasets: [
      {
        label: 'Sales Heatmap',
        data: data.values,
        backgroundColor: (context) => {
          const value = context.dataset.data[context.dataIndex].v;
          return value > 1000 ? '#ff5722' : '#4caf50';
        },
      },
    ],
  };

  return <Heatmap data={chartData} />;
}

export default SalesHeatmap;
