import React, { useState, useMemo } from 'react';
import { Download } from 'lucide-react';
import Sidebar from './components/Sidebar';
import FileUploader from './components/FileUploader';
import KPICards from './components/KPICards';
import DataTable from './components/DataTable';
import AnomalyChart from './components/AnomalyChart';
import { BillingRecord, KPIMetrics } from './types';
import { exportAnomalyData, generateSampleData } from './utils/dataExport';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [billingData, setBillingData] = useState<BillingRecord[]>([]);

  const metrics: KPIMetrics = useMemo(() => {
    if (billingData.length === 0) {
      return {
        totalRecords: 0,
        totalAnomalies: 0,
        averageBilledAmount: 0,
      };
    }

    const totalAnomalies = billingData.filter(record => record.isAnomaly).length;
    const totalAmount = billingData.reduce((sum, record) => sum + record.totalAmount, 0);
    
    return {
      totalRecords: billingData.length,
      totalAnomalies,
      averageBilledAmount: totalAmount / billingData.length,
    };
  }, [billingData]);

  const handleDataLoad = (data: BillingRecord[]) => {
    setBillingData(data);
    setActiveSection('analytics');
  };

  const handleExport = () => {
    if (billingData.length > 0) {
      exportAnomalyData(billingData);
    } else {
      // Export sample data if no data is loaded
      const sampleData = generateSampleData();
      exportAnomalyData(sampleData);
    }
  };

  const handleLoadSampleData = () => {
    const sampleData = generateSampleData();
    setBillingData(sampleData);
    setActiveSection('analytics');
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'dashboard':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-8">
              <h1 className="text-3xl font-bold text-gray-800 mb-4">
                Telecom Billing Anomaly Analyzer
              </h1>
              <p className="text-gray-600 text-lg mb-6">
                Upload your billing data to detect anomalies, analyze patterns, and generate insights 
                for better billing management and fraud detection.
              </p>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="font-semibold text-blue-800 mb-2">Key Features</h3>
                  <ul className="text-blue-700 space-y-1">
                    <li>• Automated anomaly detection</li>
                    <li>• Real-time KPI monitoring</li>
                    <li>• Data visualization</li>
                    <li>• Export capabilities</li>
                  </ul>
                </div>
                
                <div className="bg-green-50 p-6 rounded-lg">
                  <h3 className="font-semibold text-green-800 mb-2">Getting Started</h3>
                  <div className="space-y-3">
                    <button
                      onClick={() => setActiveSection('data')}
                      className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Upload Your Data
                    </button>
                    <button
                      onClick={handleLoadSampleData}
                      className="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                    >
                      Try Sample Data
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'data':
        return (
          <div className="space-y-6">
            <FileUploader onDataLoaded={handleDataLoad} />
            {billingData.length > 0 && (
              <>
                <KPICards metrics={metrics} />
                <DataTable data={billingData} />
              </>
            )}
          </div>
        );

      case 'analytics':
        return (
          <div className="space-y-6">
            {billingData.length > 0 ? (
              <>
                <KPICards metrics={metrics} />
                <AnomalyChart data={billingData} />
                <DataTable data={billingData} />
              </>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <p className="text-gray-600 mb-4">No data available for analysis.</p>
                <button
                  onClick={() => setActiveSection('data')}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Upload Data
                </button>
              </div>
            )}
          </div>
        );

      case 'export':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Export Options</h3>
              <div className="space-y-4">
                <div className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-medium text-gray-800 mb-2">Anomaly Data Export</h4>
                  <p className="text-gray-600 text-sm mb-3">
                    Export all detected anomalies as a CSV file for further analysis.
                  </p>
                  <button
                    onClick={handleExport}
                    className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors inline-flex items-center space-x-2"
                  >
                    <Download size={20} />
                    <span>Export Anomaly Data</span>
                  </button>
                </div>
                
                <div className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-medium text-gray-800 mb-2">Export Statistics</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Total Records:</span>
                      <div className="font-semibold">{metrics.totalRecords}</div>
                    </div>
                    <div>
                      <span className="text-gray-600">Anomalies:</span>
                      <div className="font-semibold text-red-600">{metrics.totalAnomalies}</div>
                    </div>
                    <div>
                      <span className="text-gray-600">Anomaly Rate:</span>
                      <div className="font-semibold">
                        {metrics.totalRecords > 0 
                          ? ((metrics.totalAnomalies / metrics.totalRecords) * 100).toFixed(1) 
                          : 0}%
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-600">Avg Amount:</span>
                      <div className="font-semibold">${metrics.averageBilledAmount.toFixed(2)}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar activeSection={activeSection} onSectionChange={setActiveSection} />
      
      <div className="flex-1 p-8">
        <div className="max-w-7xl mx-auto">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

export default App;