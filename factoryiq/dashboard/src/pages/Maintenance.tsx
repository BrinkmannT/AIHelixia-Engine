import type { FactoryDashboardResponse } from "../services/factoryApi";

interface MaintenanceProps {
  engineDashboard: FactoryDashboardResponse | null;
  onBack: () => void;
}

interface PredictionEvidence {
  evidence_strength?: string;
  evidence_count?: number;
  historical_evidence_available?: boolean;
  historical_outcome_count?: number;
  historical_average_confidence?: number | null;
  historical_support?: {
    dominant_outcome?: string | null;
  };
}

interface PredictionScenario {
  type?: string;
  source?: string;
  machine_id?: string;
  priority?: string;
  confidence?: string;
  severity?: string;
  description?: string;
  trigger_signals?: string[];
  evidence?: PredictionEvidence;
}

const labelMap: Record<string, string> = {
  potential_machine_degradation: "Mögliche Maschinenverschlechterung",
  potential_machine_risk: "Mögliches Maschinenrisiko",
  machine_warning_persistence: "Warnzustand kann anhalten",
  machine_downtime_persistence: "Möglicher Stillstand",
  machine_state_persistence: "Laufender Maschinenzustand",
  alarm_persistence: "Alarmzustand kann anhalten",
  potential_production_impact: "Mögliche Produktionsauswirkung",
  potential_energy_persistence: "Mögliche Energieauswirkung",
};

const valueMap: Record<string, string> = {
  not_available: "Nicht verfügbar",
  available: "Verfügbar",
  limited: "Eingeschränkt",
  scheduled: "Geplant",
  preventive: "Präventiv",
  running: "In Betrieb",
  stopped: "Stillstand",
  offline: "Offline",
  down: "Ausgefallen",
  warning: "Warnung",
  degraded: "Degradiert",
  high: "Hoch",
  medium: "Mittel",
  low: "Niedrig",
  strong: "Stark",
  moderate: "Mittel",
  limited_evidence: "Eingeschränkt",
  machine: "Maschine",
  industrial_analysis: "Industrieanalyse",
  anomaly_analysis: "Anomalieanalyse",
  production: "Produktion",
  energy: "Energie",
  observations: "Beobachtungen",
  entities: "Entitäten",
  conditions: "Bedingungen",
  improved: "Verbessert",
  degraded_outcome: "Verschlechtert",
  unchanged: "Unverändert",
};

function getLabel(type?: string): string {
  if (!type) return "Unbekanntes Szenario";
  return labelMap[type] ?? type.replaceAll("_", " ");
}

function formatValue(value?: unknown): string {
  if (value === undefined || value === null || value === "") {
    return "—";
  }

  const normalized = String(value);

  return valueMap[normalized] ?? normalized.replaceAll("_", " ");
}

function getPrediction(
  dashboard: FactoryDashboardResponse | null,
): Record<string, unknown> {
  return dashboard?.ai?.prediction ?? {};
}

export default function Maintenance({
  engineDashboard,
  onBack,
}: MaintenanceProps) {
  const prediction = getPrediction(engineDashboard);

  const rawScenarios = Array.isArray(prediction.scenarios)
    ? prediction.scenarios
    : [];

  const scenarios = rawScenarios.filter(
    (scenario): scenario is PredictionScenario =>
      typeof scenario === "object" && scenario !== null,
  );

  const maintenanceScenarios = scenarios.filter((scenario) =>
    [
      "potential_machine_degradation",
      "potential_machine_risk",
      "machine_warning_persistence",
      "machine_downtime_persistence",
      "machine_state_persistence",
    ].includes(scenario.type ?? ""),
  );

  const highPriority = maintenanceScenarios.filter(
    (scenario) => scenario.priority === "high",
  );

  const strongEvidence = maintenanceScenarios.filter(
    (scenario) => scenario.evidence?.evidence_strength === "strong",
  );

  const historicalSupport =
    typeof prediction.historical_support === "object" &&
    prediction.historical_support !== null
      ? (prediction.historical_support as Record<string, unknown>)
      : {};

  const maintenance = engineDashboard?.maintenance;

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <button className="back-button" onClick={onBack}>
            ← Dashboard
          </button>

          <h1>Vorausschauende Instandhaltung</h1>

          <p>
            Maschinenrisiken und bestehende Prediction-Szenarien aus der
            AIHelixia Intelligence Engine.
          </p>
        </div>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span className="kpi-label">Instandhaltungs-Szenarien</span>
          <strong>{maintenanceScenarios.length}</strong>
        </div>

        <div className="kpi-card">
          <span className="kpi-label">Hohe Priorität</span>
          <strong>{highPriority.length}</strong>
        </div>

        <div className="kpi-card">
          <span className="kpi-label">Starke Evidenz</span>
          <strong>{strongEvidence.length}</strong>
        </div>

        <div className="kpi-card">
          <span className="kpi-label">Historische Unterstützung</span>
          <strong>
            {formatValue(historicalSupport.status)}
          </strong>
        </div>
      </div>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-header">
            <div>
              <h2>Aktueller Instandhaltungsstatus</h2>
              <p>Direkt aus dem aktuellen FactoryIQ World State.</p>
            </div>
          </div>

          {maintenance ? (
            <div className="maintenance-status">
              <div>
                <span>Maschine</span>
                <strong>{maintenance.machine_id ?? "—"}</strong>
              </div>

              <div>
                <span>Status</span>
                <strong>{formatValue(maintenance.status)}</strong>
              </div>

              <div>
                <span>Typ</span>
                <strong>{formatValue(maintenance.type)}</strong>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              Keine Instandhaltungsdaten vorhanden.
            </div>
          )}
        </section>

        <section className="panel">
          <div className="panel-header">
            <div>
              <h2>Historische Unterstützung</h2>
              <p>Historische Outcome-Daten der Prediction Engine.</p>
            </div>
          </div>

          <div className="maintenance-history">
            <div>
              <span>Status</span>
              <strong>
                {formatValue(historicalSupport.status)}
              </strong>
            </div>

            <div>
              <span>Bekannte Outcomes</span>
              <strong>
                {String(historicalSupport.known_outcome_count ?? 0)}
              </strong>
            </div>

            <div>
              <span>Durchschnittliche Confidence</span>
              <strong>
                {typeof historicalSupport.average_confidence === "number"
                  ? `${Math.round(
                      historicalSupport.average_confidence * 100,
                    )}%`
                  : "—"}
              </strong>
            </div>

            <div>
              <span>Dominantes Outcome</span>
              <strong>
                {formatValue(historicalSupport.dominant_outcome)}
              </strong>
            </div>
          </div>
        </section>
      </div>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Maschinenrisiken</h2>
            <p>
              Prognostizierte Zustände und Risiken für die Instandhaltung.
            </p>
          </div>

          <span className="panel-count">
            {maintenanceScenarios.length}
          </span>
        </div>

        {maintenanceScenarios.length === 0 ? (
          <div className="empty-state">
            Aktuell liegen keine maschinenbezogenen Prediction-Szenarien vor.
          </div>
        ) : (
          <div className="maintenance-list">
            {maintenanceScenarios.map((scenario, index) => (
              <div className="maintenance-row" key={`${scenario.type}-${index}`}>
                <div className="maintenance-main">
                  <div className="maintenance-title">
                    <strong>{getLabel(scenario.type)}</strong>

                    {scenario.priority && (
                      <span
                        className={`priority-badge priority-${scenario.priority}`}
                      >
                        {scenario.priority}
                      </span>
                    )}
                  </div>

                  <p>{scenario.description ?? "Keine Beschreibung verfügbar."}</p>

                  <div className="maintenance-meta">
                    {scenario.machine_id && (
                      <span>Maschine: {scenario.machine_id}</span>
                    )}

                    {scenario.confidence && (
                      <span>Confidence: {formatValue(scenario.confidence)}</span>
                    )}

                    {scenario.severity && (
                      <span>Severity: {formatValue(scenario.severity)}</span>
                    )}

                    {scenario.source && (
                      <span>Quelle: {formatValue(scenario.source)}</span>
                    )}
                  </div>

                  {scenario.trigger_signals &&
                    scenario.trigger_signals.length > 0 && (
                      <div className="signal-list">
                        {scenario.trigger_signals.map((signal) => (
                          <span key={signal}>{signal}</span>
                        ))}
                      </div>
                    )}
                </div>

                <div className="maintenance-evidence">
                  <span>Evidenz</span>
                  <strong>
                    {formatValue(scenario.evidence?.evidence_strength)}
                  </strong>

                  {typeof scenario.evidence?.evidence_count === "number" && (
                    <small>
                      {scenario.evidence.evidence_count} Evidenzsignale
                    </small>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
