import { useMemo, useState } from "react";
import {
  anomalies,
  machines,
  maintenancePredictions,
  sensors,
} from "../services/mockData";

interface MachineDetailProps {
  machineId: string;
  onBack: () => void;
}

export default function MachineDetail({
  machineId,
  onBack,
}: MachineDetailProps) {
  const machine = machines.find((item) => item.id === machineId);

  const machineSensors = useMemo(
    () => sensors.filter((sensor) => sensor.machineId === machineId),
    [machineId],
  );

  const machineAnomalies = useMemo(
    () => anomalies.filter((anomaly) => anomaly.machineId === machineId),
    [machineId],
  );

  const prediction = maintenancePredictions.find(
    (item) => item.machineId === machineId,
  );

  if (!machine) {
    return (
      <main className="main-content">
        <button className="ghost-button" onClick={onBack}>
          ← Zurück zu Maschinen
        </button>

        <section className="placeholder-page">
          <div className="placeholder-icon">?</div>
          <span className="eyebrow">MASCHINE</span>
          <h2>Maschine nicht gefunden</h2>
          <p>Für diese Maschinen-ID liegen keine Daten vor.</p>
        </section>
      </main>
    );
  }

  const getSensor = (type: string) =>
    machineSensors.find((sensor) => sensor.type === type);

  const temperature = getSensor("temperature");
  const vibration = getSensor("vibration");
  const pressure = getSensor("pressure");
  const current = getSensor("current");

  const machineState =
    machine.status === "critical"
      ? "Kritischer Zustand"
      : machine.status === "warning"
        ? "Warnung"
        : "Betriebsbereit";

  const primaryAnomaly = machineAnomalies[0];
  const [showAnalysis, setShowAnalysis] = useState(false);

  return (
    <main className="main-content machine-detail-v4">
      <header className="machine-v4-header">
        <div className="machine-v4-heading">
          <button
            className="machine-v4-back"
            onClick={onBack}
            aria-label="Zurück zu Maschinen"
          >
            ←
          </button>

          <div>
            <div className="eyebrow">MASCHINENDETAIL</div>
            <h1>
              {machine.id} <span>·</span> {machine.name}
            </h1>
            <p>
              {machine.area} <span>•</span> {machine.productionLine}
            </p>
          </div>
        </div>

        <div className="machine-v4-live">
          <span />
          LIVE
        </div>
      </header>

      <section className="machine-v4-state">
        <div className="machine-v4-state-left">
          <span className={`status-dot ${machine.status}`} />
          <strong>{machineState}</strong>

          <span className="machine-v4-state-separator" />

          <span>
            {primaryAnomaly
              ? primaryAnomaly.title
              : "Keine kritischen Auffälligkeiten"}
          </span>
        </div>

        <div className="machine-v4-state-right">
          <span>Aktualisiert</span>
          <strong>08:45:32</strong>
        </div>
      </section>

      <section className="machine-v4-sensors">
        <SensorMetric
          label="Temperatur"
          value={temperature ? `${temperature.value} ${temperature.unit}` : "—"}
          reference={
            temperature?.normalMin !== undefined &&
            temperature.normalMax !== undefined
              ? `${temperature.normalMin}–${temperature.normalMax} ${temperature.unit}`
              : "Keine Referenz"
          }
          status={temperature?.status ?? "normal"}
        />

        <SensorMetric
          label="Schwingung"
          value={vibration ? `${vibration.value} ${vibration.unit}` : "—"}
          reference={
            vibration?.normalMin !== undefined &&
            vibration.normalMax !== undefined
              ? `${vibration.normalMin}–${vibration.normalMax} ${vibration.unit}`
              : "Keine Referenz"
          }
          status={vibration?.status ?? "normal"}
          emphasis
        />

        <SensorMetric
          label="Druck"
          value={pressure ? `${pressure.value} ${pressure.unit}` : "—"}
          reference={
            pressure?.normalMin !== undefined &&
            pressure.normalMax !== undefined
              ? `${pressure.normalMin}–${pressure.normalMax} ${pressure.unit}`
              : "Keine Referenz"
          }
          status={pressure?.status ?? "normal"}
        />

        <SensorMetric
          label="Stromaufnahme"
          value={current ? `${current.value} ${current.unit}` : "—"}
          reference={
            current?.normalMin !== undefined &&
            current.normalMax !== undefined
              ? `${current.normalMin}–${current.normalMax} ${current.unit}`
              : "Keine Referenz"
          }
          status={current?.status ?? "normal"}
        />
      </section>

      <section className="machine-v4-analysis">
        <div className="machine-v4-chart">
          <div className="machine-v4-section-header">
            <div>
              <span className="eyebrow">SENSORANALYSE</span>
              <h2>Schwingungsverlauf</h2>
            </div>

            <span className="machine-v4-period">Letzte 24 Stunden</span>
          </div>

          <div className="machine-v4-chart-summary">
            <div>
              <strong>
                {vibration ? `${vibration.value} ${vibration.unit}` : "—"}
              </strong>
              <span>Aktueller Wert</span>
            </div>

            <div className="critical-metric">
              <strong>+48%</strong>
              <span>Abweichung</span>
            </div>

            <div>
              <strong>2.0–3.5 mm/s</strong>
              <span>Normalbereich</span>
            </div>
          </div>

          <div className="machine-v4-graph">
            <div className="machine-v4-yaxis">
              <span>6.0</span>
              <span>5.0</span>
              <span>4.0</span>
              <span>3.0</span>
              <span>2.0</span>
            </div>

            <div className="machine-v4-plot">
              <div className="machine-v4-grid">
                <span />
                <span />
                <span />
                <span />
                <span />
              </div>

              <div className="machine-v4-normal-zone" />

              <svg
                viewBox="0 0 900 250"
                preserveAspectRatio="none"
                aria-label="Schwingungsverlauf"
              >
                <polyline
                  points="0,188 55,184 110,187 165,176 220,179 275,166 330,173 385,155 440,162 495,145 550,151 605,128 660,136 715,106 770,120 825,76 900,52"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="4"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <circle cx="900" cy="52" r="6" fill="currentColor" />
              </svg>

              <div className="machine-v4-anomaly">
                <span />
                <strong>Anomalie</strong>
                <b>+48%</b>
              </div>

              <div className="machine-v4-xaxis">
                <span>00:00</span>
                <span>06:00</span>
                <span>12:00</span>
                <span>18:00</span>
                <span>Jetzt</span>
              </div>
            </div>
          </div>
        </div>

        <aside className="machine-v4-diagnosis">
          <div className="machine-v4-section-header">
            <div>
              <span className="eyebrow">KI-DIAGNOSE</span>
              <h2>Ausfallrisiko</h2>
            </div>

            <span className="machine-v4-ai-badge">KI AKTIV</span>
          </div>

          {prediction ? (
            <div className="machine-v4-diagnosis-body">
              <div className="machine-v4-risk">
                <div className="machine-v4-risk-ring">
                  <strong>{prediction.failureProbability}%</strong>
                  <span>Risiko</span>
                </div>

                <div>
                  <span className="status-dot critical" />
                  <strong>Hohes Ausfallrisiko</strong>
                </div>
              </div>

              <div className="machine-v4-diagnosis-data">
                <div>
                  <span>Wahrscheinliche Komponente</span>
                  <strong>Lager</strong>
                </div>

                <div>
                  <span>Prognosefenster</span>
                  <strong>{prediction.estimatedWindow}</strong>
                </div>

                <div>
                  <span>KI-Konfidenz</span>
                  <strong>{prediction.confidence}%</strong>
                </div>
              </div>

              <div className="machine-v4-recommendation">
                <div>
                  <span>KI</span>
                  <strong>Handlungsempfehlung</strong>
                </div>

                <p>
                  Lagerprüfung einplanen und weitere
                  Vibrationsentwicklung überwachen.
                </p>
              </div>

              <button className="machine-v4-action">
                Wartungsauftrag erstellen
                <span>→</span>
              </button>
            </div>
          ) : (
            <div className="empty-state">
              <strong>Keine Ausfallprognose verfügbar</strong>
              <span>Für diese Maschine liegt aktuell kein Modell vor.</span>
            </div>
          )}
        </aside>
      </section>

      <section className="machine-v4-event">
        <div className="machine-v4-section-header">
          <div>
            <span className="eyebrow">EREIGNIS</span>
            <h2>Kritische Anomalie</h2>
          </div>

          <span className="machine-v4-event-time">Heute · 08:42</span>
        </div>

        {primaryAnomaly ? (
          <div className="machine-v4-event-body">
            <div className="machine-v4-event-status">
              <span className="status-dot critical" />
              <strong>Kritisch</strong>
            </div>

            <div className="machine-v4-event-main">
              <strong>{primaryAnomaly.title}</strong>
              <span>{primaryAnomaly.description}</span>
            </div>

            <div className="machine-v4-event-value">
              <strong>{primaryAnomaly.value}</strong>
              <span>Abweichung</span>
            </div>

            <div className="machine-v4-event-confidence">
              <strong>{primaryAnomaly.aiConfidence ?? "—"}%</strong>
              <span>KI-Konfidenz</span>
            </div>

            <button
              className="machine-v4-event-action"
              onClick={() => setShowAnalysis((current) => !current)}
            >
              {showAnalysis ? "Analyse schließen ↑" : "Analyse öffnen →"}
            </button>
          </div>
        ) : (
          <div className="empty-state">
            <strong>Keine aktiven Anomalien</strong>
            <span>Die Maschine befindet sich im normalen Betriebsbereich.</span>
          </div>
        )}
      </section>

      {showAnalysis && (
        <section className="machine-v4-ai-analysis">
          <div className="machine-v4-section-header">
            <div>
              <span className="eyebrow">AIHELIXIA INTELLIGENCE ENGINE</span>
              <h2>KI-Analyse der Schwingungsanomalie</h2>
            </div>

            <span className="machine-v4-analysis-status">
              ANALYSE ABGESCHLOSSEN
            </span>
          </div>

          <div className="machine-v4-analysis-grid">
            <div className="machine-v4-analysis-main">
              <div className="machine-v4-analysis-intro">
                <span className="status-dot critical" />
                <div>
                  <strong>Schwingungsanomalie erkannt</strong>
                  <span>
                    Der aktuelle Messwert liegt deutlich über dem
                    historischen Normalbereich.
                  </span>
                </div>
              </div>

              <div className="machine-v4-analysis-metrics">
                <div>
                  <span>Abweichung</span>
                  <strong>+48%</strong>
                </div>

                <div>
                  <span>Ausfallrisiko</span>
                  <strong>87%</strong>
                </div>

                <div>
                  <span>KI-Konfidenz</span>
                  <strong>92%</strong>
                </div>
              </div>

              <div className="machine-v4-cause-section">
                <span className="eyebrow">WAHRSCHEINLICHE URSACHE</span>

                <div className="machine-v4-primary-cause">
                  <span>01</span>
                  <div>
                    <strong>Pumpenlager</strong>
                    <p>
                      Das erkannte Schwingungsmuster ist mit einem
                      beginnenden Lagerproblem vereinbar.
                    </p>
                  </div>
                </div>

                <div className="machine-v4-secondary-causes">
                  <div>
                    <span>02</span>
                    <strong>Unwucht</strong>
                  </div>

                  <div>
                    <span>03</span>
                    <strong>Mechanische Belastung</strong>
                  </div>
                </div>
              </div>
            </div>

            <aside className="machine-v4-analysis-action">
              <span className="eyebrow">EMPFOHLENE MASSNAHME</span>

              <h3>Lagerprüfung einplanen</h3>

              <p>
                Eine technische Prüfung der Lagerung sollte innerhalb
                des prognostizierten Zeitfensters durchgeführt werden.
                Die weitere Vibrationsentwicklung sollte bis dahin
                überwacht werden.
              </p>

              <div className="machine-v4-analysis-window">
                <span>Empfohlenes Zeitfenster</span>
                <strong>18–30 Stunden</strong>
              </div>

              <button className="machine-v4-action">
                Wartungsauftrag erstellen
                <span>→</span>
              </button>
            </aside>
          </div>
        </section>
      )}

      <section className="machine-v4-bottom">
        <div className="machine-v4-maintenance">
          <div className="machine-v4-section-header">
            <div>
              <span className="eyebrow">INSTANDHALTUNG</span>
              <h2>Wartungsstatus</h2>
            </div>
          </div>

          <div className="machine-v4-maintenance-status">
            <div className="machine-v4-maintenance-icon">⚙</div>

            <div>
              <strong>Wartung empfohlen</strong>
              <span>
                Sensorentwicklung und KI-Prognose erfordern eine Prüfung.
              </span>
            </div>
          </div>

          <div className="machine-v4-maintenance-row">
            <span>Letzte Wartung</span>
            <strong>Vor 23 Tagen</strong>
          </div>

          <div className="machine-v4-maintenance-row">
            <span>Nächste geplante Wartung</span>
            <strong>In 12 Tagen</strong>
          </div>
        </div>

        <div className="machine-v4-masterdata">
          <div className="machine-v4-section-header">
            <div>
              <span className="eyebrow">STAMMDATEN</span>
              <h2>Maschineninformationen</h2>
            </div>
          </div>

          <div className="machine-v4-master-grid">
            <div>
              <span>Maschine</span>
              <strong>{machine.name}</strong>
            </div>

            <div>
              <span>Bereich</span>
              <strong>{machine.area}</strong>
            </div>

            <div>
              <span>Produktionslinie</span>
              <strong>{machine.productionLine}</strong>
            </div>

            <div>
              <span>Status</span>
              <strong>{machineState}</strong>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function SensorMetric({
  label,
  value,
  reference,
  status,
  emphasis = false,
}: {
  label: string;
  value: string;
  reference: string;
  status: string;
  emphasis?: boolean;
}) {
  const statusLabel =
    status === "critical"
      ? "Kritisch"
      : status === "warning"
        ? "Warnung"
        : "Normal";

  return (
    <div className={`machine-v4-sensor ${emphasis ? "is-emphasis" : ""}`}>
      <div className="machine-v4-sensor-head">
        <span>{label}</span>
        <i className={`status-dot ${status}`} />
      </div>

      <strong>{value}</strong>

      <div className="machine-v4-sensor-bottom">
        <span>{reference}</span>
        <b>{statusLabel}</b>
      </div>
    </div>
  );
}
