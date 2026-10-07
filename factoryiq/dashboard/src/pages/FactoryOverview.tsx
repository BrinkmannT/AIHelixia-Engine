import type { FactoryDashboardResponse } from "../services/factoryApi";

interface FactoryOverviewProps {
  engineDashboard: FactoryDashboardResponse | null;
  onBack: () => void;
}

export default function FactoryOverview({
  engineDashboard,
  onBack,
}: FactoryOverviewProps) {
  if (!engineDashboard) {
    return (
      <main className="main-content">
        <section className="placeholder-page">
          <span className="eyebrow">FACTORYIQ</span>
          <h2>Keine Verbindung zur Engine</h2>
          <p>Die Werksdaten konnten nicht geladen werden.</p>
          <button className="ghost-button" onClick={onBack}>
            ← Dashboard
          </button>
        </section>
      </main>
    );
  }

  const { factory, kpis, machines, sensors, alarms, production, energy, maintenance } =
    engineDashboard;

  const machineCount = machines.machines.length;
  const sensorCount = sensors.sensors.length;
  const alarmCount = alarms.alarms.length;

  return (
    <main className="main-content">
      <header className="topbar">
        <div>
          <div className="eyebrow">FACTORYIQ LEITSTAND</div>
          <h1>Werksübersicht</h1>
          <p>
            {factory.name ?? "Factory"} · {factory.location ?? "—"}
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
          <h2>{factory.name ?? "Werk"}</h2>
          <p>
            Zentraler Überblick über Anlagenzustand, Produktion, Energie und
            Alarme
          </p>
        </div>

        <button className="ghost-button" onClick={onBack}>
          ← Dashboard
        </button>
      </section>

      <section className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-header">
            <span>MASCHINEN</span>
            <span className="kpi-status healthy">●</span>
          </div>
          <strong>{machineCount}</strong>
          <div className="kpi-footer">
            <span>Aktive Anlagen</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>SENSOREN</span>
            <span className="kpi-status healthy">●</span>
          </div>
          <strong>{sensorCount}</strong>
          <div className="kpi-footer">
            <span>Erfasste Sensoren</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>ALARME</span>
            <span className="kpi-status warning">●</span>
          </div>
          <strong>{alarmCount}</strong>
          <div className="kpi-footer">
            <span>
              Kritisch: {alarms.severity_counts.critical ?? 0}
            </span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>WERKSSTATUS</span>
            <span className="kpi-status healthy">●</span>
          </div>
          <strong>{factory.status ?? "—"}</strong>
          <div className="kpi-footer">
            <span>Aktueller Zustand</span>
          </div>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">ANLAGEN</span>
              <h3>Maschinen im Werk</h3>
            </div>
          </div>

          <div className="machine-table">
            {machines.machines.map((machine) => (
              <div className="machine-row" key={machine.id}>
                <span className="status-dot normal" />
                <div>
                  <strong>{machine.id}</strong>
                  <span>{machine.name ?? "Maschine"}</span>
                </div>
                <span>
                  {machine.production_line_id ?? "Keine Linie"}
                </span>
                <b className="machine-state normal">
                  {(machine.status ?? "unknown").toUpperCase()}
                </b>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">PRODUKTION</span>
              <h3>Produktionszustand</h3>
            </div>
          </div>

          <div className="ai-insight">
            <span>AKTUELLER OUTPUT</span>
            <strong>
              {kpis.production_output ?? "—"} /{" "}
              {kpis.production_target ?? "—"}
            </strong>
            <p>
              Status:{" "}
              {typeof production.status === "string"
                ? production.status
                : "nicht verfügbar"}
            </p>
          </div>
        </div>
      </section>

      <section className="dashboard-grid lower-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">ENERGIE</span>
              <h3>Energieverbrauch</h3>
            </div>
          </div>

          <div className="ai-insight">
            <span>AKTUELLER VERBRAUCH</span>
            <strong>
              {kpis.energy_consumption ?? "—"}{" "}
              {kpis.energy_unit ?? ""}
            </strong>
            <p>
              Status:{" "}
              {typeof energy.status === "string"
                ? energy.status
                : "nicht verfügbar"}
            </p>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">INSTANDHALTUNG</span>
              <h3>Maintenance Status</h3>
            </div>
          </div>

          <div className="ai-insight">
            <span>AKTUELLER STATUS</span>
            <strong>
              {typeof maintenance.status === "string"
                ? maintenance.status
                : "nicht verfügbar"}
            </strong>
            <p>
              Maschine:{" "}
              {typeof maintenance.machine_id === "string"
                ? maintenance.machine_id
                : "—"}
            </p>
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <span className="eyebrow">ALARME</span>
            <h3>Aktuelle Werksalarme</h3>
          </div>
        </div>

        <div className="anomaly-list">
          {alarms.alarms.map((alarm) => (
            <div className="anomaly-row" key={alarm.id}>
              <div className={`priority ${alarm.severity.toLowerCase()}`}>
                {alarm.severity}
              </div>

              <div className="anomaly-main">
                <strong>{alarm.machine_id}</strong>
                <span>{alarm.message ?? alarm.type ?? "Alarm"}</span>
              </div>

              <div className="anomaly-value">{alarm.type ?? "—"}</div>

              <time>
                {new Date(alarm.timestamp).toLocaleTimeString("de-DE", {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </time>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
