export type StreamMessage = {
    type: 'metric';
    data: { metric: string; value: number; ts: string };
    alert: boolean;
    zscore: number;
  };
  
  export type SnapshotState = {
    selectedMetric: string;
    timeRangeHours: number;
    layout?: 'default' | 'dense';
  };
  