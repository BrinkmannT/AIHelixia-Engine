import { useEffect, useState } from "react";
import "./App.css";

type Machine = {
  id: string;
  name: string;
  production_line_id: string;
  status: string;
};

type Alarm = {
  id: string;
  timestamp: string;
  machine_id: string;
  severity: string;
  type: string;
  message: string;
};

type DashboardData = {
  status: string;
  version: string;
  factory: {
    id: string;
    name: string;
    location: string;
    status: string;
  };
  kpis: {
    machine_count: number;
    alarm_count: number;
    production_output: number;
    production_target: number;
    energy_consumption: number;
    energy_unit: string;
  };
  machines: {
    status_counts: Record<string, number>;
    machines: Machine[];
  };
  alarms: {
    severity_counts: Record<string, number>;
    alarms: Alarm[];
  };
  production: {
    timestamp: string;
    output: number;
    target: number;
    status: string;
  };
  energy: {
    timestamp: string;
    consumption: number;
    unit: string;
    status: string;
  };
  maintenance: {
    machine_id: string;
    timestamp: string;
    status: string;
    type: string;
  };
  ai: {
    operational_signal: string;
    learning_signal: {
      type: string;
      priority: string;
      reason: string;
    };
    prediction: {
      scenario: string;
      confidence: number;
    };
    decision: {
      status: string;
      decision_type: string;
      action: string;
      rationale: string;
      scenario_count: number;
    };
    evaluation: {
      status: string;
      evaluation: string;
      score: number;
      message: string;
      action_status: string;
    };
  };
  historical_patterns: {
    recurring_machine_ids: string[];
    machine_counts: Record<string, number>;
    status_counts: Record<string, number>;
    entry_count: number;
  };
};

const navItems = [
  ["⌂", "Dashboard"],
  ["▦", "Werke"],
  ["◈", "Produktion"],
  ["⚙", "Maschinen"],
  ["△", "Anomalien"],
  ["◷", "Predictive Maintenance"],
  ["◇", "Qualität"],
  ["ϟ", "Energie"],
  ["◉", "OEE & Performance"],
  ["▤", "Aufträge"],
  ["▥", "Material & Lager"],
  ["▣", "Reports"],
  ["✦", "KI Insights"],
  ["⚙", "Einstellungen"],
];

const trendPoints = [
  [6, 58],
  [12, 55],
  [18, 57],
  [24, 51],
  [30, 54],
  [36, 47],
  [42, 49],
  [48, 42],
  [54, 45],
  [60, 40],
  [66, 44],
  [72, 37],
  [78, 39],
  [84, 34],
  [90, 36],
  [96, 31],
];

function formatTime(timestamp?: string) {
  if (!timestamp) return "--:--";
  const date = new Date(timestamp);
  return date.toLocaleTimeString("de-DE", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatLabel(value: string) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function linePath(offset = 0, scale = 1) {
  return trendPoints
    .map(([x, y], index) => {
      const adjusted = Math.max(8, Math.min(92, y + offset + Math.sin(index) * 3 * scale));
      return `${index === 0 ? "M" : "L"} ${x} ${adjusted}`;
    })
    .join(" ");
}

function Panel({
  title,
  eyebrow,
  children,
  action,
  className = "",
}: {
  title: string;
  eyebrow?: string;
  children: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}) {
  return (
    <section className={`panel ${className}`}>
      <div className="panel-header">
        <div>
          {eyebrow && <div className="panel-eyebrow">{eyebrow}</div>}
          <h2>{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}

function MiniChart({
  variant = "green",
  bars = false,
}: {
  variant?: "green" | "blue" | "red" | "yellow";
  bars?: boolean;
}) {
  if (bars) {
    return (
      <div className="mini-bars">
        {Array.from({ length: 15 }).map((_, index) => (
          <span
            key={index}
            style={{
              height: `${30 + ((index * 17) % 65)}%`,
            }}
          />
        ))}
      </div>
    );
  }

  return (
    <svg className={`mini-chart ${variant}`} viewBox="0 0 100 60" preserveAspectRatio="none">
      <path d={linePath(variant === "red" ? 12 : variant === "yellow" ? 6 : 0)} />
    </svg>
  );
}

function KpiCard({
  label,
  value,
  unit,
  change,
  variant = "green",
  bars = false,
}: {
  label: string;
  value: string;
  unit?: string;
  change: string;
  variant?: "green" | "blue" | "red" | "yellow";
  bars?: boolean;
}) {
  return (
    <div className={`kpi-card ${variant}`}>
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">
        {value}
        {unit && <span>{unit}</span>}
      </div>
      <div className="kpi-bottom">
        <span className="kpi-change">{change}</span>
        <MiniChart variant={variant} bars={bars} />
      </div>
    </div>
  );
}

function App() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState("");
  const [lastUpdate, setLastUpdate] = useState(new Date());

  async function loadDashboard() {
    try {
      const response = await fetch("/api/factory/dashboard");

      if (!response.ok) {
        const body = await response.text();
        throw new Error(body || `HTTP ${response.status}`);
      }

      const dashboard = await response.json();
      setData(dashboard);
      setError("");
      setLastUpdate(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Dashboard konnte nicht geladen werden.");
    }
  }

  useEffect(() => {
    loadDashboard();

    const interval = window.setInterval(loadDashboard, 15000);
    return () => window.clearInterval(interval);
  }, []);

  const activeMachine = data?.machines.machines[0];

  if (!data && !error) {
    return (
      <div className="loading-screen">
        <div className="loading-logo">FQ</div>
        <strong>FactoryIQ Command Center</strong>
        <span>Verbindung zur Intelligence Engine wird hergestellt …</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="loading-screen">
        <div className="error-box">
          <strong>FactoryIQ API nicht erreichbar</strong>
          <span>{error}</span>
          <button onClick={loadDashboard}>Erneut verbinden</button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const alarmCount = data.kpis.alarm_count;
  const criticalCount = data.alarms.severity_counts.critical ?? 0;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <span />
            <span />
            <span />
          </div>
          <div>
            <div className="brand-name">
              Factory<span>IQ</span>
            </div>
            <div className="brand-subtitle">Manufacturing Intelligence</div>
          </div>
        </div>

        <nav className="navigation">
          {navItems.map(([icon, label], index) => (
            <button
              key={label}
              className={`nav-item ${index === 0 ? "active" : ""}`}
            >
              <span className="nav-icon">{icon}</span>
              <span>{label}</span>
              {label === "Anomalien" && alarmCount > 0 && (
                <span className="nav-count">{alarmCount}</span>
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="plant-selector">
            <div className="plant-icon">◇</div>
            <div>
              <strong>Werk {data.factory.location}</strong>
              <span>
                <i className="online-dot" /> Online
              </span>
            </div>
            <span className="chevron">⌃</span>
          </div>

          <div className="user-card">
            <div className="avatar">TB</div>
            <div>
              <strong>Administrator</strong>
              <span>FactoryIQ Operator</span>
            </div>
          </div>

          <div className="edition">
            <div className="edition-logo">✕</div>
            <div>
              <strong>FactoryIQ</strong>
              <span>Enterprise Edition</span>
            </div>
            <small>v1.0.0</small>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="search-box">
            <span>⌕</span>
            <input placeholder="Suche (Maschine, Auftrag, Störung, ...)" />
            <kbd>⌘ K</kbd>
          </div>

          <div className="topbar-right">
            <div className="clock">
              <span>
                {new Date().toLocaleDateString("de-DE", {
                  weekday: "short",
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}
              </span>
              <strong>
                {new Date().toLocaleTimeString("de-DE", {
                  hour: "2-digit",
                  minute: "2-digit",
                  second: "2-digit",
                })}
              </strong>
            </div>

            <div className="system-state">
              <i />
              <div>
                <strong>Alle Systeme online</strong>
                <span>Werk {data.factory.location}</span>
              </div>
            </div>

            <button className="icon-button">♧<b>{alarmCount}</b></button>
            <button className="icon-button">⚙</button>
            <button className="fullscreen-button">↗</button>
          </div>
        </header>

        <div className="content">
          <section className="page-heading">
            <div>
              <h1>FactoryIQ Command Center</h1>
              <p>Realtime-Transparenz. Höhere Effizienz. Weniger Stillstand.</p>
            </div>
            <div className="heading-actions">
              <button className="select-button">Letzte 24 Stunden　⌄</button>
              <button className="primary-button">⇩ Exportieren</button>
              <button className="more-button">•••</button>
            </div>
          </section>

          <section className="kpi-grid">
            <KpiCard
              label="OEE (Gesamt)"
              value="87,6"
              unit="%"
              change="↑ +4,3%"
            />
            <KpiCard
              label="Verfügbarkeit"
              value="92,1"
              unit="%"
              change="↑ +3,7%"
            />
            <KpiCard
              label="Leistung"
              value="84,3"
              unit="%"
              change="↑ +2,1%"
              variant="blue"
            />
            <KpiCard
              label="Qualität"
              value="95,2"
              unit="%"
              change="↑ +1,8%"
            />
            <KpiCard
              label="Ausschussquote"
              value="2,34"
              unit="%"
              change="↓ -0,41%"
              variant="red"
            />
            <KpiCard
              label="Energieverbrauch"
              value="1,23"
              unit=" MWh"
              change="↓ -6,7%"
              variant="blue"
            />
            <KpiCard
              label="Aktive Alarme"
              value={String(alarmCount)}
              change={`${criticalCount} kritisch`}
              variant="red"
              bars
            />
          </section>

          <section className="dashboard-grid top-grid">
            <Panel
              title={`Werksübersicht – Werk ${data.factory.location}`}
              className="factory-panel"
              action={
                <div className="view-switch">
                  <button className="selected">3D</button>
                  <button>2D</button>
                  <button>Liste</button>
                </div>
              }
            >
              <div className="factory-map">
                <div className="map-grid" />
                <div className="factory-building building-a">HALLE 1</div>
                <div className="factory-building building-b">HALLE 2</div>
                <div className="factory-building building-c">HALLE 3</div>
                <div className="factory-building building-d">HALLE 4</div>

                <div className="map-marker marker-green marker-1">
                  <b>●</b>
                  <span>Halle 1<strong>OEE 91,2%</strong></span>
                </div>

                <div className="map-marker marker-yellow marker-2">
                  <b>●</b>
                  <span>Halle 2<strong>OEE 78,4%</strong></span>
                </div>

                <div className="map-marker marker-green marker-3">
                  <b>●</b>
                  <span>Halle 3<strong>OEE 88,9%</strong></span>
                </div>

                <div className="map-marker marker-yellow marker-4">
                  <b>●</b>
                  <span>Halle 4<strong>OEE 94,1%</strong></span>
                </div>

                <div className="map-marker marker-red marker-energy">
                  <b>●</b>
                  <span>Energiezentrale<strong>Störung</strong></span>
                </div>

                <div className="map-controls">
                  <button>+</button>
                  <button>−</button>
                </div>
              </div>

              <div className="factory-stats">
                <div>
                  <span className="stat-icon">☁</span>
                  <div><small>Wetter</small><strong>16°C</strong><em>{data.factory.location}</em></div>
                </div>
                <div>
                  <span className="stat-icon green">◉</span>
                  <div><small>Produktion</small><strong>Aktiv</strong></div>
                </div>
                <div>
                  <span className="stat-icon blue">♙</span>
                  <div><small>Mitarbeiter</small><strong>248</strong></div>
                </div>
                <div>
                  <span className="stat-icon yellow">▤</span>
                  <div><small>Aufträge</small><strong>12</strong></div>
                </div>
                <div>
                  <span className="stat-icon green">✧</span>
                  <div><small>Materialstatus</small><strong>Normal</strong></div>
                </div>
              </div>
            </Panel>

            <div className="stack-column">
              <Panel
                title="Aktuelle Anomalien"
                action={<button className="text-button">Alle anzeigen ({alarmCount})</button>}
              >
                <div className="alarm-list">
                  {data.alarms.alarms.length > 0 ? (
                    data.alarms.alarms.map((alarm) => (
                      <div className="alarm-row" key={alarm.id}>
                        <span className={`severity ${alarm.severity}`}>
                          {alarm.severity === "critical" ? "▲ Kritisch" : "▲ Warnung"}
                        </span>
                        <div>
                          <strong>{alarm.message}</strong>
                          <small>{alarm.machine_id} · {formatLabel(alarm.type)}</small>
                        </div>
                        <time>{formatTime(alarm.timestamp)}</time>
                      </div>
                    ))
                  ) : (
                    <div className="empty-state">Keine aktiven Anomalien</div>
                  )}
                </div>
              </Panel>

              <Panel
                title="Nächste Wartungen"
                action={<button className="text-button">Alle anzeigen</button>}
              >
                <div className="maintenance-list">
                  {[
                    ["Presse P-12", "in 3 Tagen", "Hoch"],
                    ["Extruder E-03", "in 7 Tagen", "Mittel"],
                    ["Kompressor K-07", "in 11 Tagen", "Mittel"],
                    ["Trockner T-02", "in 14 Tagen", "Niedrig"],
                    ["Pumpe P-08", "in 18 Tagen", "Niedrig"],
                  ].map(([name, date, priority]) => (
                    <div className="maintenance-row" key={name}>
                      <strong>{name}</strong>
                      <span>{date}</span>
                      <b className={`priority ${priority.toLowerCase()}`}>{priority}</b>
                    </div>
                  ))}
                </div>
              </Panel>
            </div>

            <div className="stack-column">
              <Panel
                title="Top KPI Trends (7 Tage)"
                action={<button className="select-small">7 Tage　⌄</button>}
              >
                <div className="chart large-chart">
                  <div className="chart-axis">
                    <span>100%</span>
                    <span>75%</span>
                    <span>50%</span>
                    <span>25%</span>
                    <span>0%</span>
                  </div>
                  <svg viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path className="chart-line green-line" d={linePath(0)} />
                    <path className="chart-line blue-line" d={linePath(10, 0.8)} />
                    <path className="chart-line yellow-line" d={linePath(22, 1)} />
                    <path className="chart-line purple-line" d={linePath(-7, 0.7)} />
                    <path className="chart-line red-line" d={linePath(38, 0.6)} />
                  </svg>
                </div>
                <div className="legend">
                  <span className="green-dot">● OEE</span>
                  <span className="blue-dot">● Verfügbarkeit</span>
                  <span className="yellow-dot">● Leistung</span>
                  <span className="purple-dot">● Qualität</span>
                  <span className="red-dot">● Ausschuss</span>
                </div>
              </Panel>

              <Panel
                title="Energieverbrauch"
                action={<button className="select-small">Letzte 24 Stunden　⌄</button>}
              >
                <div className="big-metric blue-green">
                  {data.energy.consumption.toFixed(2).replace(".", ",")} <span>{data.energy.unit === "kWh" ? "kWh" : data.energy.unit}</span>
                  <small>↓ -6,7% vs. gestern</small>
                </div>
                <div className="energy-bars">
                  {Array.from({ length: 24 }).map((_, index) => (
                    <span key={index} style={{ height: `${25 + ((index * 31) % 70)}%` }} />
                  ))}
                </div>
                <div className="chart-footer">
                  <span>Heute</span>
                  <span>Gestern</span>
                </div>
              </Panel>
            </div>
          </section>

          <section className="dashboard-grid bottom-grid">
            <Panel
              title="Produktionsverlauf (OEE)"
              action={<button className="select-small">Letzte 24 Stunden　⌄</button>}
            >
              <div className="production-chart">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none">
                  <path className="chart-line green-line" d={linePath(3)} />
                  <path className="chart-line blue-line" d={linePath(8)} />
                  <path className="chart-line yellow-line" d={linePath(18)} />
                  <path className="chart-line purple-line" d={linePath(-5)} />
                </svg>
              </div>
              <div className="legend">
                <span className="green-dot">● Linie 1</span>
                <span className="blue-dot">● Linie 2</span>
                <span className="yellow-dot">● Linie 3</span>
                <span className="purple-dot">● Linie 4</span>
              </div>
            </Panel>

            <Panel
              title="Aktive Produktionsaufträge"
              action={<button className="text-button">Alle Aufträge</button>}
            >
              <div className="orders">
                {[
                  ["A-2026-001", "Bauteil A", "10.000", "8.450", 85, "In Produktion"],
                  ["A-2026-002", "Gehäuse B", "5.000", "5.000", 100, "Abgeschlossen"],
                  ["A-2026-003", "Modul C", "7.500", "6.200", 83, "In Produktion"],
                  ["A-2026-004", "Komponente D", "3.000", "1.200", 40, "Verzögert"],
                  ["A-2026-005", "Bauteil E", "12.000", "9.800", 82, "In Produktion"],
                ].map(([id, product, target, actual, progress, status]) => (
                  <div className="order-row" key={id}>
                    <strong>{id}</strong>
                    <span>{product}</span>
                    <span>{target}</span>
                    <span>{actual}</span>
                    <div className="progress"><i style={{ width: `${progress}%` }} /></div>
                    <b className={status === "Verzögert" ? "delayed" : status === "Abgeschlossen" ? "complete" : ""}>
                      {status}
                    </b>
                  </div>
                ))}
              </div>
            </Panel>

            <Panel
              title="Qualität – Erste-Pass-Rate"
              action={<button className="select-small">Letzte 24 Stunden　⌄</button>}
            >
              <div className="quality-value">
                98,1% <span>↑ +1,3% vs. gestern</span>
              </div>
              <div className="quality-chart">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none">
                  <path className="chart-line green-line" d={linePath(-12, 0.45)} />
                </svg>
              </div>
              <div className="quality-footer">
                <span>● Erste-Pass-Rate</span>
                <span>— Zielwert (95%)</span>
              </div>
            </Panel>
          </section>

          <section className="insights-section">
            <div className="insights-heading">KI Insights & Empfehlungen</div>

            <div className="insights-grid">
              <div className="insight-card">
                <div className="insight-icon blue">✦</div>
                <div className="insight-content">
                  <strong>Potenzial zur Effizienzsteigerung</strong>
                  <p>
                    Die AIHelixia Engine hat 3 Optimierungspotenziale identifiziert,
                    die die OEE um bis zu 4,7% steigern könnten.
                  </p>
                </div>
                <button>Details anzeigen</button>
              </div>

              <div className="insight-card">
                <div className="insight-icon green">ϟ</div>
                <div className="insight-content">
                  <strong>Energieoptimierung</strong>
                  <p>
                    Verbrauch in Halle 3 liegt 12% über dem erwarteten Wert.
                    Ursache könnte ein ineffizienter Kühlkreislauf sein.
                  </p>
                </div>
                <button>Analyse starten</button>
              </div>

              <div className="insight-card">
                <div className="insight-icon blue">⚒</div>
                <div className="insight-content">
                  <strong>Wartung vor Ausfall</strong>
                  <p>
                    {activeMachine?.id ?? "MACHINE-001"} zeigt einen steigenden
                    Zustandsindikator. Empfohlene Wartung innerhalb der nächsten 72 Stunden.
                  </p>
                </div>
                <button>Wartung planen</button>
              </div>
            </div>
          </section>

          <footer className="dashboard-footer">
            <span>AIHelixia Intelligence Engine</span>
            <span>FactoryIQ Enterprise Edition · Live API · localhost:8000</span>
            <span>Letzte Aktualisierung: {lastUpdate.toLocaleTimeString("de-DE")}</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
