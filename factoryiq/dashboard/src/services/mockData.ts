import type {
  AIInsight,
  Anomaly,
  KPI,
  Machine,
  MaintenancePrediction,
  Plant,
  Sensor,
  SystemHealth,
  Tenant,
  WorkOrder,
} from "../types";

export const pckSchwedt: Plant = {
  id: "pck-schwedt",
  name: "PCK Schwedt",
  location: "Schwedt/Oder, Brandenburg",
  status: "operational",
};

export const pckTenant: Tenant = {
  id: "pck-schwedt-pilot",
  displayName: "PCK Schwedt – Pilot",
  demo: true,
  plant: pckSchwedt,
};

export const machines: Machine[] = [
  {
    id: "P-12",
    name: "Pump P-12",
    area: "Raffinerie",
    status: "critical",
    productionLine: "Line 01",
  },
  {
    id: "E-03",
    name: "Heater E-03",
    area: "Energiezentrale",
    status: "critical",
    productionLine: "Energy 01",
  },
  {
    id: "K-07",
    name: "Valve K-07",
    area: "Versorgung",
    status: "warning",
    productionLine: "Supply 02",
  },
  {
    id: "T-02",
    name: "Tank T-02",
    area: "Tanklager",
    status: "warning",
    productionLine: "Storage 01",
  },
  {
    id: "M-05",
    name: "Motor M-05",
    area: "Instandhaltung",
    status: "normal",
    productionLine: "Line 03",
  },
  {
    id: "F-01",
    name: "Fan F-01",
    area: "Energiezentrale",
    status: "normal",
    productionLine: "Energy 02",
  },
  {
    id: "R-101",
    name: "Reactor R-101",
    area: "Raffinerie",
    status: "normal",
    productionLine: "Line 04",
  },
];

export const sensors: Sensor[] = [
  {
    id: "P12-VIB",
    machineId: "P-12",
    type: "vibration",
    value: 5.17,
    unit: "mm/s",
    normalMin: 2.0,
    normalMax: 3.5,
    status: "critical",
    timestamp: "2026-09-28T08:42:00",
  },
  {
    id: "P12-TEMP",
    machineId: "P-12",
    type: "temperature",
    value: 72.4,
    unit: "°C",
    normalMin: 45,
    normalMax: 70,
    status: "warning",
    timestamp: "2026-09-28T08:42:00",
  },
  {
    id: "E03-TEMP",
    machineId: "E-03",
    type: "temperature",
    value: 218,
    unit: "°C",
    normalMin: 185,
    normalMax: 200,
    status: "critical",
    timestamp: "2026-09-28T08:31:00",
  },
  {
    id: "K07-PRESS",
    machineId: "K-07",
    type: "pressure",
    value: 8.7,
    unit: "bar",
    normalMin: 7.5,
    normalMax: 8.0,
    status: "warning",
    timestamp: "2026-09-28T08:14:00",
  },
  {
    id: "T02-ENERGY",
    machineId: "T-02",
    type: "current",
    value: 108,
    unit: "kW",
    normalMin: 90,
    normalMax: 100,
    status: "warning",
    timestamp: "2026-09-28T07:56:00",
  },
];

export const anomalies: Anomaly[] = [
  {
    id: "ANOM-P12-001",
    machineId: "P-12",
    title: "Vibration anomaly",
    description:
      "Vibrationsmuster liegt deutlich über dem historischen Normalbereich.",
    priority: "CRITICAL",
    value: "+48%",
    deviation: 48,
    detectedAt: "2026-09-28T08:42:00",
    status: "investigating",
    aiConfidence: 92,
  },
  {
    id: "ANOM-E03-001",
    machineId: "E-03",
    title: "Temperature deviation",
    description:
      "Temperatur des Heizsystems überschreitet den definierten Betriebsbereich.",
    priority: "CRITICAL",
    value: "+18°C",
    deviation: 18,
    detectedAt: "2026-09-28T08:31:00",
    status: "open",
    aiConfidence: 88,
  },
  {
    id: "ANOM-K07-001",
    machineId: "K-07",
    title: "Pressure fluctuation",
    description:
      "Druckschwankung oberhalb des historischen Toleranzbereichs.",
    priority: "WARNING",
    value: "+11%",
    deviation: 11,
    detectedAt: "2026-09-28T08:14:00",
    status: "investigating",
    aiConfidence: 81,
  },
  {
    id: "ANOM-T02-001",
    machineId: "T-02",
    title: "Energy consumption",
    description:
      "Energieverbrauch liegt über dem erwarteten Verbrauchsprofil.",
    priority: "WARNING",
    value: "+8%",
    deviation: 8,
    detectedAt: "2026-09-28T07:56:00",
    status: "open",
    aiConfidence: 76,
  },
  {
    id: "ANOM-M05-001",
    machineId: "M-05",
    title: "Cycle time deviation",
    description:
      "Leichte Abweichung der Zykluszeit vom historischen Mittelwert.",
    priority: "INFO",
    value: "+3%",
    deviation: 3,
    detectedAt: "2026-09-28T07:38:00",
    status: "open",
    aiConfidence: 69,
  },
];

export const maintenancePredictions: MaintenancePrediction[] = [
  {
    id: "PRED-P12",
    machineId: "P-12",
    component: "Pump bearing",
    failureProbability: 87,
    estimatedWindow: "18–30 Stunden",
    confidence: 92,
    recommendation:
      "Lagerprüfung einplanen und Vibrationsentwicklung weiter überwachen.",
  },
  {
    id: "PRED-E03",
    machineId: "E-03",
    component: "Heating element",
    failureProbability: 62,
    estimatedWindow: "2–4 Tage",
    confidence: 84,
    recommendation:
      "Heizelement und Temperaturregelung bei nächstem Wartungsfenster prüfen.",
  },
  {
    id: "PRED-K07",
    machineId: "K-07",
    component: "Control valve",
    failureProbability: 48,
    estimatedWindow: "5–7 Tage",
    confidence: 78,
    recommendation:
      "Ventilsteuerung und Druckverlauf kontrollieren.",
  },
  {
    id: "PRED-T02",
    machineId: "T-02",
    component: "Energy sensor",
    failureProbability: 35,
    estimatedWindow: "7–14 Tage",
    confidence: 73,
    recommendation:
      "Sensorprüfung im nächsten geplanten Wartungsfenster durchführen.",
  },
];

export const kpis: KPI[] = [
  {
    id: "oee",
    label: "OEE",
    value: "87.6%",
    numericValue: 87.6,
    trend: 2.4,
    status: "normal",
  },
  {
    id: "availability",
    label: "Availability",
    value: "92.1%",
    numericValue: 92.1,
    trend: 1.8,
    status: "normal",
  },
  {
    id: "performance",
    label: "Performance",
    value: "84.3%",
    numericValue: 84.3,
    trend: 3.1,
    status: "normal",
  },
  {
    id: "quality",
    label: "Quality",
    value: "95.2%",
    numericValue: 95.2,
    trend: 0.7,
    status: "normal",
  },
  {
    id: "scrap",
    label: "Scrap",
    value: "2.34%",
    numericValue: 2.34,
    trend: -0.4,
    status: "normal",
  },
  {
    id: "energy",
    label: "Energy",
    value: "12.8 GWh",
    numericValue: 12.8,
    unit: "GWh",
    trend: -3.2,
    status: "normal",
  },
  {
    id: "alarms",
    label: "Active Alarms",
    value: "7",
    numericValue: 7,
    trend: 2,
    status: "warning",
  },
];

export const aiInsights: AIInsight[] = [
  {
    id: "AI-P12-001",
    title: "P-12 erhöhtes Ausfallrisiko",
    description:
      "Das aktuelle Vibrationsmuster weicht deutlich vom historischen Normalbereich ab.",
    confidence: 92,
    severity: "critical",
    machineId: "P-12",
    recommendation:
      "Inspektion des Pumpenlagers innerhalb von 18–30 Stunden einplanen.",
  },
  {
    id: "AI-E03-001",
    title: "E-03 Temperaturtrend",
    description:
      "Der Temperaturtrend zeigt eine kontinuierliche Abweichung vom Referenzprofil.",
    confidence: 88,
    severity: "warning",
    machineId: "E-03",
    recommendation:
      "Heizsystem und Temperaturregelung überprüfen.",
  },
];

export const workOrders: WorkOrder[] = [
  {
    id: "WO-2026-0912",
    machineId: "P-12",
    title: "Pumpenlager prüfen",
    priority: "critical",
    status: "planned",
    scheduledFor: "2026-09-29",
  },
  {
    id: "WO-2026-0913",
    machineId: "E-03",
    title: "Heizelement überprüfen",
    priority: "high",
    status: "open",
    scheduledFor: "2026-10-01",
  },
];

export const systemHealth: SystemHealth = {
  backend: "online",
  aiEngine: "online",
  database: "online",
  lastUpdate: "2026-09-28T08:45:00",
};
