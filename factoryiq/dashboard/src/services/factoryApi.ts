export interface FactoryMaintenance {
  machine_id?: string;
  status?: string;
  type?: string;
}

export interface FactoryDashboardResponse {
  status: string;
  version: string;

  factory: {
    id?: string;
    name?: string;
    location?: string;
    status?: string;
  };

  kpis: {
    machine_count: number;
    alarm_count: number;
    production_output?: number;
    production_target?: number;
    energy_consumption?: number;
    energy_unit?: string;
  };

  machines: {
    status_counts: Record<string, number>;
    machines: Array<{
      id: string;
      name?: string;
      production_line_id?: string;
      status?: string;
    }>;
  };

  sensors: {
    sensors: Array<{
      id?: string;
      name?: string;
      machine_id: string;
      type: string;
      unit?: string;
      value?: number;
    }>;
  };

  alarms: {
    severity_counts: Record<string, number>;
    alarms: Array<{
      id: string;
      timestamp: string;
      machine_id: string;
      severity: string;
      type?: string;
      message?: string;
    }>;
  };

  production: Record<string, unknown>;
  energy: Record<string, unknown>;
  maintenance: FactoryMaintenance;

  ai: {
    operational_signal?: string;
    anomaly_analysis?: {
      status?: string;
      severity?: string;
      signal_count?: number;
      signals?: Array<{
        type?: string;
        machine_id?: string;
        sensor_id?: string;
        value?: number;
        unit?: string;
        threshold?: number;
        target?: number;
        ratio?: number;
        severity?: string;
        alarm_id?: string;
      }>;
      signal_types?: string[];
      correlated_machines?: string[];
      machine_signal_counts?: Record<string, number>;
      critical_alarm_count?: number;
      confidence?: number;
      production_output?: number;
      production_target?: number;
      energy_value?: number;
    };
    learning_signal?: Record<string, unknown>;
    prediction?: Record<string, unknown>;
    decision?: Record<string, unknown>;
    evaluation?: Record<string, unknown>;
  };

  historical_patterns: {
    recurring_machine_ids: string[];
    machine_counts: Record<string, number>;
    status_counts: Record<string, number>;
    entry_count: number;
  };
}

const API_BASE_URL = "http://127.0.0.1:8000";

export async function getFactoryDashboard(): Promise<FactoryDashboardResponse> {
  const response = await fetch(`${API_BASE_URL}/factory/dashboard`);

  if (!response.ok) {
    throw new Error(
      `FactoryIQ API Fehler: ${response.status} ${response.statusText}`,
    );
  }

  return response.json() as Promise<FactoryDashboardResponse>;
}
