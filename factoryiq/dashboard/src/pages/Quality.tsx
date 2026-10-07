import type { FactoryDashboardResponse } from "../services/factoryApi";

interface QualityProps {
  engineDashboard: FactoryDashboardResponse | null;
  onBack: () => void;
}

const valueMap: Record<string, string> = {
  no_anomaly: "Keine Anomalie",
  anomaly_signal: "Anomaliesignal",
  anomaly_detected: "Anomalie erkannt",
  none: "Keine",
  low: "Niedrig",
  medium: "Mittel",
  high: "Hoch",
  critical: "Kritisch",
  vibration_elevated: "Erhöhte Vibration",
  temperature_elevated: "Erhöhte Temperatur",
  production_decreased: "Produktionsrückgang",
  energy_increased: "Erhöhter Energieverbrauch",
  critical_alarm: "Kritischer Alarm",
};

function translate(value: string | undefined): string {
  if (!value) return "—";
  return valueMap[value] ?? value;
}

export default function Quality({
  engineDashboard,
  onBack,
}: QualityProps) {
  if (!engineDashboard) {
    return (
      <main className="page-content">
        <button className="back-button" onClick={onBack}>
          ← Zurück
        </button>

        <section className="page-header">
          <div>
            <span className="eyebrow">QUALITÄT</span>
            <h1>Qualitätsintelligenz</h1>
            <p>Keine Engine-Daten verfügbar.</p>
          </div>
        </section>

        <section className="empty-state">
          <strong>AIHelixia Engine nicht erreichbar</strong>
          <span>
            Die Qualitätsanalyse kann erst angezeigt werden, wenn aktuelle
            Engine-Daten verfügbar sind.
          </span>
        </section>
      </main>
    );
  }

  const anomaly = engineDashboard.ai.anomaly_analysis;

  if (!anomaly) {
    return (
      <main className="page-content">
        <button className="back-button" onClick={onBack}>
          ← Zurück
        </button>

        <section className="page-header">
          <div>
            <span className="eyebrow">QUALITÄT</span>
            <h1>Qualitätsintelligenz</h1>
            <p>Analyse des aktuellen Produktionszustands</p>
          </div>
        </section>

        <section className="empty-state">
          <strong>Noch keine Anomalieanalyse verfügbar</strong>
          <span>
            Die AIHelixia Engine hat aktuell keine Anomalieanalyse an das
            Dashboard geliefert.
          </span>
        </section>
      </main>
    );
  }

  const signals = Array.isArray(anomaly.signals)
    ? anomaly.signals
    : [];

  const correlatedMachines = Array.isArray(
    anomaly.correlated_machines
  )
    ? anomaly.correlated_machines
    : [];

  const productionOutput = anomaly.production_output;
  const productionTarget = anomaly.production_target;

  const productionRatio =
    typeof productionOutput === "number" &&
    typeof productionTarget === "number" &&
    productionTarget > 0
      ? productionOutput / productionTarget
      : null;

  return (
    <main className="page-content">
      <button className="back-button" onClick={onBack}>
        ← Zurück
      </button>

      <section className="page-header">
        <div>
          <span className="eyebrow">QUALITÄT</span>
          <h1>Qualitätsintelligenz</h1>
          <p>
            Qualitäts- und Produktionsrisiken aus der aktuellen
            AIHelixia-Analyse
          </p>
        </div>

        <div className={`priority-badge ${anomaly.severity}`}>
          {translate(anomaly.severity)}
        </div>
      </section>

      <section className="kpi-grid">
        <article className="kpi-card">
          <span>Status</span>
          <strong>{translate(anomaly.status)}</strong>
          <small>Aktuelle Anomalieanalyse</small>
        </article>

        <article className="kpi-card">
          <span>Signale</span>
          <strong>{anomaly.signal_count}</strong>
          <small>Erkannte Risikosignale</small>
        </article>

        <article className="kpi-card">
          <span>Konfidenz</span>
          <strong>
            {typeof anomaly.confidence === "number"
              ? `${Math.round(anomaly.confidence * 100)} %`
              : "—"}
          </strong>
          <small>Engine-Konfidenz</small>
        </article>

        <article className="kpi-card">
          <span>Betroffene Maschinen</span>
          <strong>{correlatedMachines.length}</strong>
          <small>Korrelierte Maschinen</small>
        </article>
      </section>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">RISIKOSIGNALE</span>
              <h2>Erkannte Qualitätsrisiken</h2>
            </div>
            <span className="panel-count">{signals.length}</span>
          </div>

          {signals.length === 0 ? (
            <div className="empty-state">
              <strong>Keine Risikosignale</strong>
              <span>
                Aktuell wurden keine qualitätsrelevanten Anomalien erkannt.
              </span>
            </div>
          ) : (
            <div className="quality-signal-list">
              {signals.map((signal, index) => (
                <div
                  className="quality-signal"
                  key={`${signal.type}-${index}`}
                >
                  <div className="quality-signal-main">
                    <strong>{translate(signal.type)}</strong>

                    <span>
                      {signal.machine_id
                        ? `Maschine ${signal.machine_id}`
                        : "Produktionssystem"}
                    </span>
                  </div>

                  <div className="quality-signal-value">
                    {typeof signal.value === "number"
                      ? `${signal.value}${
                          signal.unit ? ` ${signal.unit}` : ""
                        }`
                      : signal.severity
                        ? translate(signal.severity)
                        : "—"}
                  </div>
                </div>
              ))}
            </div>
          )}
        </article>

        <article className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">PRODUKTION</span>
              <h2>Produktionsqualität</h2>
            </div>
          </div>

          <div className="quality-metric">
            <span>Output</span>
            <strong>
              {typeof productionOutput === "number"
                ? productionOutput
                : "—"}
            </strong>
          </div>

          <div className="quality-metric">
            <span>Target</span>
            <strong>
              {typeof productionTarget === "number"
                ? productionTarget
                : "—"}
            </strong>
          </div>

          <div className="quality-metric">
            <span>Target-Erreichung</span>
            <strong>
              {productionRatio !== null
                ? `${Math.round(productionRatio * 100)} %`
                : "—"}
            </strong>
          </div>
        </article>
      </section>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">MASCHINENRISIKO</span>
              <h2>Korrelierte Maschinen</h2>
            </div>
          </div>

          {correlatedMachines.length === 0 ? (
            <div className="empty-state">
              <strong>Keine Korrelation erkannt</strong>
              <span>
                Es wurde aktuell keine Maschine mit mehreren Risikosignalen
                identifiziert.
              </span>
            </div>
          ) : (
            <div className="machine-risk-list">
              {correlatedMachines.map((machineId) => (
                <div className="machine-risk-row" key={machineId}>
                  <div>
                    <strong>{machineId}</strong>
                    <span>Mehrere korrelierte Risikosignale</span>
                  </div>

                  <span className="priority-badge high">
                    Hoch
                  </span>
                </div>
              ))}
            </div>
          )}
        </article>

        <article className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">ENGINE-BEWERTUNG</span>
              <h2>Aktuelle Einordnung</h2>
            </div>
          </div>

          <div className="quality-assessment">
            <div>
              <span>Severity</span>
              <strong>{translate(anomaly.severity)}</strong>
            </div>

            <div>
              <span>Signaltypen</span>
              <strong>
                {Array.isArray(anomaly.signal_types)
                  ? anomaly.signal_types.length
                  : 0}
              </strong>
            </div>

            <div>
              <span>Confidence</span>
              <strong>
                {typeof anomaly.confidence === "number"
                  ? `${Math.round(anomaly.confidence * 100)} %`
                  : "—"}
              </strong>
            </div>
          </div>
        </article>
      </section>
    </main>
  );
}
