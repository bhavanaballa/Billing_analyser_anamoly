import { BillingRecord } from '../types';

export const exportAnomalyData = (data: BillingRecord[]) => {
  const anomalies = data.filter(record => record.isAnomaly);
  
  // Convert to CSV format
  const headers = ['ID', 'Customer Name', 'Phone Number', 'Billing Period', 'Total Amount', 'Data Usage', 'Call Minutes', 'SMS Count'];
  const csvContent = [
    headers.join(','),
    ...anomalies.map(record => [
      record.id,
      record.customerName,
      record.phoneNumber,
      record.billingPeriod,
      record.totalAmount,
      record.dataUsage,
      record.callMinutes,
      record.smsCount
    ].join(','))
  ].join('\n');

  // Create and trigger download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `anomaly_data_${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

export const generateSampleData = (): BillingRecord[] => {
  const sampleData: BillingRecord[] = [];
  
  for (let i = 1; i <= 50; i++) {
    sampleData.push({
      id: `BILL-${String(i).padStart(4, '0')}`,
      customerName: `Customer ${i}`,
      phoneNumber: `+1-${Math.random().toString().slice(2, 5)}-${Math.random().toString().slice(2, 5)}-${Math.random().toString().slice(2, 6)}`,
      billingPeriod: '2024-01',
      totalAmount: Math.floor(Math.random() * 200) + 50,
      dataUsage: Math.floor(Math.random() * 10) + 1,
      callMinutes: Math.floor(Math.random() * 500) + 100,
      smsCount: Math.floor(Math.random() * 100) + 20,
      isAnomaly: Math.random() > 0.85, // 15% anomaly rate
    });
  }
  
  return sampleData;
};