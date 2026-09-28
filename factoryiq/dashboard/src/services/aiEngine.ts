import type {
  AIInsight,
  Anomaly,
  MaintenancePrediction,
  SystemHealth,
} from "../types";

export interface AIEngineClient {
  health(): Promise<SystemHealth>;
  analyzeAnomaly(anomaly: Anomaly): Promise<AIInsight>;
  predictFailure(machineId: string): Promise<MaintenancePrediction | undefined>;
  generateInsight(machineId?: string): Promise<AIInsight | undefined>;
  recommendAction(anomaly: Anomaly): Promise<string>;
}

export class MockAIEngineClient implements AIEngineClient {
  async health(): Promise<SystemHealth> {
    return {
      backend: "online",
      aiEngine: "online",
      database: "online",
      lastUpdate: new Date().toISOString(),
    };
  }

  async analyzeAnomaly(anomaly: Anomaly): Promise<AIInsight> {
    return {
      id: `AI-${anomaly.id}`,
      title: `${anomaly.machineId}: ${anomaly.title}`,
      description:
        anomaly.description ||
        "AI-Analyse der erkannten industriellen Anomalie.",
      confidence: anomaly.aiConfidence ?? 80,
      severity:
        anomaly.priority === "CRITICAL"
          ? "critical"
          : anomaly.priority === "WARNING"
            ? "warning"
            : "info",
      machineId: anomaly.machineId,
      recommendation: await this.recommendAction(anomaly),
    };
  }

  async predictFailure(
    _machineId: string,
  ): Promise<MaintenancePrediction | undefined> {
    return undefined;
  }

  async generateInsight(
    _machineId?: string,
  ): Promise<AIInsight | undefined> {
    return undefined;
  }

  async recommendAction(anomaly: Anomaly): Promise<string> {
    if (anomaly.machineId === "P-12") {
      return "Pumpenlager prüfen und Vibrationsentwicklung weiter überwachen.";
    }

    if (anomaly.machineId === "E-03") {
      return "Heizelement und Temperaturregelung überprüfen.";
    }

    if (anomaly.machineId === "K-07") {
      return "Ventilsteuerung und Druckverlauf kontrollieren.";
    }

    if (anomaly.machineId === "T-02") {
      return "Energieverbrauch und Sensorik überprüfen.";
    }

    return "Anlage weiter überwachen und Ursache der Abweichung prüfen.";
  }
}

export const aiEngine: AIEngineClient = new MockAIEngineClient();
