
import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import { useQuery } from 'react-query';
import { apiClient } from '../services/apiClient';
import { TextField, Button } from '@material-ui/core';
import LoadingSpinner from './LoadingSpinner';

function SalesForecastChart() {
  const [futureDates, setFutureDates] = useState(['2023-12-01', '2023-12-02']);
  const { data, isLoading, error, refetch } = useQuery(
    ['salesForecast', futureDates],
    async () => {
      const response = await apiClient.get('/ai/predict-sales/', {
        params: { future_dates: futureDates },
      });
      return response.data;
    },
    {
      enabled: false, // Disabled by default, manual refetch
    }
  );

  const handlePredict = () => {
    refetch();
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <p>Error loading sales forecast data.</p>;

  const chartData = data
    ? {
        labels: futureDates,
        datasets: [
          {
            label: 'Predicted Sales',
            data: data.predictions,
            fill: false,
            backgroundColor: '#ff9800',
            borderColor: '#ff9800',
          },
        ],
      }
    : null;

  return (
    <div>
      <TextField
        label="Future Dates (comma-separated)"
        value={futureDates.join(', ')}
        onChange={(e) => setFutureDates(e.target.value.split(',').map((date) => date.trim()))}
        fullWidth
        variant="outlined"
      />
      <Button variant="contained" color="primary" onClick={handlePredict} style={{ marginTop: 10 }}>
        Predict Sales
      </Button>
      {chartData && <Line data={chartData} />}
    </div>
  );
}

export default SalesForecastChart;
