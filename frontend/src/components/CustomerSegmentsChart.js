import React from 'react';
import { Scatter } from 'react-chartjs-2';
import { useQuery } from 'react-query';
import { apiClient } from '../services/apiClient';
import LoadingSpinner from './LoadingSpinner';

function CustomerSegmentsChart() {
  const { data, isLoading, error } = useQuery('customerSegments', async () => {
    const response = await apiClient.get('/ai/segment-customers/');
    return response.data;
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <p>Error loading customer segments.</p>;

  const chartData = {
    datasets: data.map((segment) => ({
      label: `Segment ${segment.segment}`,
      data: [{ x: segment.total, y: segment.order_count }],
      backgroundColor: getSegmentColor(segment.segment),
    })),
  };

  function getSegmentColor(segment) {
    const colors = ['#e57373', '#64b5f6', '#81c784'];
    return colors[segment % colors.length];
  }

  return <Scatter data={chartData} />;
}

export default CustomerSegmentsChart;
