export interface BillingRecord {
  id: string;
  customerName: string;
  phoneNumber: string;
  billingPeriod: string;
  totalAmount: number;
  dataUsage: number;
  callMinutes: number;
  smsCount: number;
  isAnomaly: boolean;
}

export interface KPIMetrics {
  totalRecords: number;
  totalAnomalies: number;
  averageBilledAmount: number;
}