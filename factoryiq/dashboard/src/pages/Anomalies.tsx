import type { FactoryDashboardResponse } from "../services/factoryApi";

interface AnomaliesProps {
  engineDashboard: FactoryDashboardResponse | null;
  onBack: () => void;
}

interface PredictionEvidence {
  evidence_count?: number;
  supporting_signals?: string[];
  correlated_machines?: string[];
  historical_support?: string;
  confidence_level?: string;
  evidence_strength?: string;
}

interface PredictionScenario {
  type?: string;
  source?: string;
  priority?: string;
  confidence?: string;
  machine_id?: string;
  severity?: string;
  trigger_signals?: string[];
  description?: string;
  evidence?: PredictionEvidence;
}

function textValue(value: unknown, fallback = "—"): string {
  return typeof value === "string" ? value : fallback;
}

function arrayValue(value: unknown): string[] {
  return Array.isArray(value)
    ? value.filter((item): item is string => typeof item === "string")
    : [];
}

export default function Anomalies({
  engineDashboard,
  onBack,
}: AnomaliesProps) {
  const prediction = engineDashboard?.ai.prediction;

  const scenarios: PredictionScenario[] =
    prediction && Array.isArray(prediction.scenarios)
      ? prediction.scenarios.filter(
          (scenario): scenario is PredictionScenario =>
            typeof scenario === "object" && scenario !== null,
        )
      : [];

  const highPriority = scenarios.filter(
    (scenario) => scenario.priority?.toLowerCase() === "high",
  );

  const strongEvidence = scenarios.filter(
    (scenario) => scenario.evidence?.evidence_strength === "strong",
  );

  return (
    <main className="main-content">
      <header className="topbar">
        <div>
          <div className="eyebrow">FACTORYIQ LEITSTAND</div>
          <h1>Anomalien</h1>
          <p>
            KI-basierte Erkennung und Bewertung industrieller Auffälligkeiten
          </p>
        </div>

        <div className="topbar-actions">
          <div className="live-indicator">
            <span />
            LIVE
          </div>
          <div className="user-avatar">TB</div>
        </div>
      </header>

      <section className="hero-row">
        <div>
          <h2>KI-Anomalieanalyse</h2>
          <p>
            Aktuelle Prediction-Szenarien und Evidenz aus der AIHelixia Engine
          </p>
        </div>

        <button className="ghost-button" onClick={onBack}>
          ← Dashboard
        </button>
      </section>

      {!engineDashboard ? (
        <section className="placeholder-page">
          <span className="eyebrow">AIHELIXIA ENGINE</span>
          <h2>Engine nicht verbunden</h2>
          <p>
            Es konnten keine aktuellen Anomalieinformationen geladen werden.
          </p>
        </section>
      ) : (
        <>
          <section className="kpi-grid">
            <div className="kpi-card">
              <div className="kpi-header">
                <span>Prediction-Szenarien</span>
                <span className="kpi-status healthy">●</span>
              </div>
              <strong>{scenarios.length}</strong>
              <div className="kpi-footer">
                <span>Aktuelle Analyse</span>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-header">
                <span>Hohe Priorität</span>
                <span className="kpi-status warning">●</span>
              </div>
              <strong>{highPriority.length}</strong>
              <div className="kpi-footer">
                <span>Erhöhtes Risiko</span>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-header">
                <span>Starke Evidenz</span>
                <span className="kpi-status healthy">●</span>
              </div>
              <strong>{strongEvidence.length}</strong>
              <div className="kpi-footer">
                <span>Evidence Strength</span>
              </div>
            </div>

            <div className="kpi-card">
              <div className="kpi-header">
                <span>Operational Signal</span>
                <span className="kpi-status warning">●</span>
              </div>
              <strong>
                {textValue(engineDashboard.ai.operational_signal)}
              </strong>
              <div className="kpi-footer">
                <span>Aktueller Betriebsindikator</span>
              </div>
            </div>
          </section>

          <section className="panel">
            <div className="panel-header">
              <div>
                <span className="eyebrow">AIHELIXIA PREDICTION</span>
                <h3>Erkannte Szenarien</h3>
              </div>
            </div>

            <div className="anomaly-list">
              {scenarios.length === 0 ? (
                <div className="ai-insight">
                  <span>KEINE SZENARIEN</span>
                  <strong>Aktuell liegen keine Prediction-Szenarien vor.</strong>
                </div>
              ) : (
                scenarios.map((scenario, index) => {
                  const priority = textValue(scenario.priority, "low");
                  const evidence = scenario.evidence ?? {};
                  const signals = arrayValue(scenario.trigger_signals);

                  return (
                    <div className="anomaly-row" key={`${scenario.type}-${index}`}>
                      <div className={`priority ${priority.toLowerCase()}`}>
                        {priority}
                      </div>

                      <div className="anomaly-main">
                        <strong>
                          {textValue(scenario.type, "Unbekanntes Szenario")}
                        </strong>
                        <span>
                          {textValue(
                            scenario.description,
                            "Keine Beschreibung verfügbar.",
                          )}
                        </span>

                        {scenario.machine_id && (
                          <small>Maschine: {scenario.machine_id}</small>
                        )}
                      </div>

                      <div className="anomaly-value">
                        {textValue(scenario.confidence, "—")}
                      </div>

                      <div>
                        <small>
                          Evidenz:{" "}
                          {textValue(evidence.evidence_strength, "—")}
                        </small>
                        {signals.length > 0 && (
                          <small>{signals.join(", ")}</small>
                        )}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </section>

          <section className="dashboard-grid lower-grid">
            <div className="panel">
              <div className="panel-header">
                <div>
                  <span className="eyebrow">ROOT CAUSE</span>
                  <h3>Ursachenbewertung</h3>
                </div>
              </div>

              <div className="ai-insight">
                <span>AKTUELLE ENTSCHEIDUNG</span>
                <strong>
                  {textValue(
                    engineDashboard.ai.decision &&
                      typeof engineDashboard.ai.decision.root_cause === "object"
                      ? (
                          engineDashboard.ai.decision.root_cause as Record<
                            string,
                            unknown
                          >
                        ).primary_type
                      : undefined,
                    "Keine Root-Cause-Bewertung",
                  )}
                </strong>
                <p>
                  Die Darstellung verwendet die von der Engine gelieferte
                  Root-Cause-Bewertung ohne zusätzliche Interpretation im
                  Frontend.
                </p>
              </div>
            </div>

            <div className="panel">
              <div className="panel-header">
                <div>
                  <span className="eyebrow">EVIDENZ</span>
                  <h3>Analysequalität</h3>
                </div>
              </div>

              <div className="machine-status-summary">
                <div>
                  <strong>{strongEvidence.length}</strong>
                  <small>Starke Evidenz</small>
                </div>

                <div>
                  <strong>{highPriority.length}</strong>
                  <small>Hohe Priorität</small>
                </div>

                <div>
                  <strong>
                    {textValue(
                      prediction &&
                        typeof prediction.evidence_summary === "object"
                        ? (
                            prediction.evidence_summary as Record<
                              string,
                              unknown
                            >
                          ).total_evidence_count
                        : undefined,
                      "—",
                    )}
                  </strong>
                  <small>Evidenzpunkte</small>
                </div>
              </div>
            </div>
          </section>
        </>
      )}
    </main>
  );
}
