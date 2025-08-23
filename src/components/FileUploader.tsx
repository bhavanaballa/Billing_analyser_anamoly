import React, { useCallback } from 'react';
import { Upload, FileText } from 'lucide-react';
import Papa from 'papaparse';
import { BillingRecord } from '../types';

interface FileUploaderProps {
  onDataLoaded: (data: BillingRecord[]) => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onDataLoaded }) => {
  const handleFileUpload = useCallback((file: File) => {
    Papa.parse(file, {
      complete: (results) => {
        const data = results.data as any[];
        if (data.length > 0) {
          // Convert CSV data to BillingRecord format
          const billingData: BillingRecord[] = data.slice(1).map((row, index) => ({
            id: `BILL-${String(index + 1).padStart(4, '0')}`,
            customerName: row[0] || `Customer ${index + 1}`,
            phoneNumber: row[1] || `+1-${Math.random().toString().slice(2, 5)}-${Math.random().toString().slice(2, 5)}-${Math.random().toString().slice(2, 6)}`,
            billingPeriod: row[2] || '2024-01',
            totalAmount: parseFloat(row[3]) || Math.floor(Math.random() * 200) + 50,
            dataUsage: parseFloat(row[4]) || Math.floor(Math.random() * 10) + 1,
            callMinutes: parseInt(row[5]) || Math.floor(Math.random() * 500) + 100,
            smsCount: parseInt(row[6]) || Math.floor(Math.random() * 100) + 20,
            isAnomaly: Math.random() > 0.85, // 15% anomaly rate
          }));
          onDataLoaded(billingData);
        }
      },
      header: false,
      skipEmptyLines: true,
    });
  }, [onDataLoaded]);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'text/csv') {
      handleFileUpload(file);
    }
  }, [handleFileUpload]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  }, [handleFileUpload]);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Upload Billing Data</h3>
      
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors duration-200"
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onDragEnter={(e) => e.preventDefault()}
      >
        <Upload size={48} className="mx-auto text-gray-400 mb-4" />
        <p className="text-gray-600 mb-4">
          Drag and drop your CSV file here, or click to select
        </p>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg cursor-pointer hover:bg-blue-700 transition-colors duration-200 inline-flex items-center space-x-2"
        >
          <FileText size={20} />
          <span>Select CSV File</span>
        </label>
      </div>
    </div>
  );
};

export default FileUploader;