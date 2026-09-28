export type MachineStatus = "normal" | "warning" | "critical";

export type AnomalyPriority =
  | "INFO"
  | "WARNING"
  | "CRITICAL";

export interface Plant {
  id: string;
  name: string;
  location: string;
  status: "operational" | "warning" | "offline";
}

export interface Machine {
  id: string;
  name: string;
  area: string;
  status: MachineStatus;
  productionLine?: string;
}

export interface Sensor {
  id: string;
  machineId: string;
  type: "temperature" | "vibration" | "pressure" | "current" | "rpm" | "throughput";
  value: number;
  unit: string;
  normalMin?: number;
  normalMax?: number;
  status: MachineStatus;
  timestamp: string;
}

export interface Anomaly {
  id: string;
  machineId: string;
  title: string;
  description: string;
  priority: AnomalyPriority;
  value: string;
  deviation?: number;
  detectedAt: string;
  status: "open" | "investigating" | "resolved";
  aiConfidence?: number;
}

export interface MaintenancePrediction {
  id: string;
  machineId: string;
  component: string;
  failureProbability: number;
  estimatedWindow: string;
  confidence: number;
  recommendation: string;
}

export interface KPI {
  id: string;
  label: string;
  value: string;
  numericValue?: number;
  unit?: string;
  trend: number;
  status: MachineStatus;
}

export interface AIInsight {
  id: string;
  title: string;
  description: string;
  confidence: number;
  severity: "info" | "warning" | "critical";
  machineId?: string;
  recommendation?: string;
}

export interface WorkOrder {
  id: string;
  machineId: string;
  title: string;
  priority: "low" | "medium" | "high" | "critical";
  status: "open" | "planned" | "in_progress" | "completed";
  scheduledFor?: string;
}

export interface SystemHealth {
  backend: "online" | "offline";
  aiEngine: "online" | "offline";
  database: "online" | "offline";
  lastUpdate: string;
}

export interface Tenant {
  id: string;
  displayName: string;
  demo: boolean;
  plant: Plant;
}
