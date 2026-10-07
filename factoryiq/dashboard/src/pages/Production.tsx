import type { FactoryDashboardResponse } from "../services/factoryApi";

interface ProductionProps {
  engineDashboard: FactoryDashboardResponse | null;
  onBack: () => void;
}

export default function Production({
  engineDashboard,
  onBack,
}: ProductionProps) {
  const production = engineDashboard?.production ?? {};

  const output =
    engineDashboard?.kpis.production_output ??
    (typeof production.output === "number" ? production.output : null);

  const target =
    engineDashboard?.kpis.production_target ??
    (typeof production.target === "number" ? production.target : null);

  const status =
    typeof production.status === "string"
      ? production.status
      : engineDashboard?.factory.status ?? "unknown";

  const achievement =
    output !== null && target !== null && target > 0
      ? Math.round((output / target) * 100)
      : null;

  return (
    <main className="main-content">
      <header className="topbar">
        <div>
          <div className="eyebrow">FACTORYIQ LEITSTAND</div>
          <h1>Produktion</h1>
          <p>
            {engineDashboard?.factory.name ?? "Factory"} ·{" "}
            {engineDashboard?.factory.location ?? "—"}
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
          <h2>Produktionsübersicht</h2>
          <p>
            Aktueller Produktionsstatus und Zielerreichung aus der
            AIHelixia-Engine
          </p>
        </div>

        <button className="ghost-button" onClick={onBack}>
          ← Dashboard
        </button>
      </section>

      <section className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-header">
            <span>Produktion</span>
            <span className="kpi-status healthy">●</span>
          </div>

          <strong>{output ?? "—"}</strong>

          <div className="kpi-footer">
            <span>Aktueller Output</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>Produktionsziel</span>
            <span className="kpi-status healthy">●</span>
          </div>

          <strong>{target ?? "—"}</strong>

          <div className="kpi-footer">
            <span>Aktuelles Ziel</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>Zielerreichung</span>
            <span className="kpi-status healthy">●</span>
          </div>

          <strong>{achievement !== null ? `${achievement}%` : "—"}</strong>

          <div className="kpi-footer">
            <span>Output / Ziel</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span>Status</span>
            <span className="kpi-status healthy">●</span>
          </div>

          <strong>{status}</strong>

          <div className="kpi-footer">
            <span>Produktionszustand</span>
          </div>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">PRODUKTION</span>
              <h3>Aktueller Produktionszustand</h3>
            </div>
          </div>

          <div className="ai-insight">
            <span>FACTORYIQ ENGINE</span>
            <strong>
              {output !== null && target !== null
                ? `${output} von ${target} Produktionseinheiten erreicht.`
                : "Keine ausreichenden Produktionsdaten verfügbar."}
            </strong>
            <p>
              Der dargestellte Wert stammt direkt aus dem aktuellen
              FactoryIQ-Dashboard-Datensatz.
            </p>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">ANLAGENSTATUS</span>
              <h3>Produktionsstatus</h3>
            </div>
          </div>

          <div className="machine-status-summary">
            <div>
              <span className="status-dot normal" />
              <strong>{status}</strong>
              <small>Aktueller Zustand</small>
            </div>

            <div>
              <strong>{engineDashboard?.machines.machines.length ?? 0}</strong>
              <small>Maschinen</small>
            </div>

            <div>
              <strong>{engineDashboard?.kpis.alarm_count ?? 0}</strong>
              <small>Alarme</small>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
