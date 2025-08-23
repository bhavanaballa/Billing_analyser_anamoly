import React from 'react';
import { Users, AlertTriangle, DollarSign } from 'lucide-react';
import { KPIMetrics } from '../types';

interface KPICardsProps {
  metrics: KPIMetrics;
}

const KPICards: React.FC<KPICardsProps> = ({ metrics }) => {
  const kpis = [
    {
      title: 'Total Records',
      value: metrics.totalRecords.toLocaleString(),
      icon: Users,
      color: 'blue',
      bgColor: 'bg-blue-50',
      iconColor: 'text-blue-600',
    },
    {
      title: 'Anomalies Detected',
      value: metrics.totalAnomalies.toLocaleString(),
      icon: AlertTriangle,
      color: 'red',
      bgColor: 'bg-red-50',
      iconColor: 'text-red-600',
    },
    {
      title: 'Avg Billed Amount',
      value: `$${metrics.averageBilledAmount.toFixed(2)}`,
      icon: DollarSign,
      color: 'green',
      bgColor: 'bg-green-50',
      iconColor: 'text-green-600',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      {kpis.map((kpi) => {
        const Icon = kpi.icon;
        return (
          <div
            key={kpi.title}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">{kpi.title}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{kpi.value}</p>
              </div>
              <div className={`${kpi.bgColor} p-3 rounded-full`}>
                <Icon className={`${kpi.iconColor} w-6 h-6`} />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default KPICards;