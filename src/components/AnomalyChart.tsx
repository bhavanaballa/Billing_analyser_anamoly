import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { BillingRecord } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface AnomalyChartProps {
  data: BillingRecord[];
}

const AnomalyChart: React.FC<AnomalyChartProps> = ({ data }) => {
  const normalCount = data.filter(record => !record.isAnomaly).length;
  const anomalyCount = data.filter(record => record.isAnomaly).length;

  const chartData = {
    labels: ['Normal Bills', 'Anomaly Bills'],
    datasets: [
      {
        label: 'Number of Bills',
        data: [normalCount, anomalyCount],
        backgroundColor: [
          'rgba(16, 185, 129, 0.8)', // Green for normal
          'rgba(239, 68, 68, 0.8)',  // Red for anomalies
        ],
        borderColor: [
          'rgba(16, 185, 129, 1)',
          'rgba(239, 68, 68, 1)',
        ],
        borderWidth: 2,
        borderRadius: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Billing Anomaly Analysis',
        font: {
          size: 16,
          weight: 'bold' as const,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  if (data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Anomaly Analysis</h3>
        <div className="flex items-center justify-center h-64 text-gray-500">
          Upload data to see anomaly analysis
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default AnomalyChart;