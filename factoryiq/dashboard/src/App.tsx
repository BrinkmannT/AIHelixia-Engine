import { useState } from "react";
import "./App.css";
import Machines from "./pages/Machines";
import MachineDetail from "./pages/MachineDetail";
import { anomalies as demoAnomalies, kpis as demoKpis, machines as demoMachines } from "./services/mockData";

type Page =
  | "Dashboard"
  | "Werksübersicht"
  | "Produktion"
  | "Maschinen"
  | "Anomalien"
  | "Vorausschauende Instandhaltung"
  | "Qualität"
  | "Energie"
  | "OEE & Leistung"
  | "Aufträge"
  | "Material & Lager"
  | "Berichte"
  | "KI-Erkenntnisse"
  | "Einstellungen";

const navigation: { icon: string; label: Page }[] = [
  { icon: "⌂", label: "Dashboard" },
  { icon: "▦", label: "Werksübersicht" },
  { icon: "◈", label: "Produktion" },
  { icon: "⚙", label: "Maschinen" },
  { icon: "△", label: "Anomalien" },
  { icon: "◷", label: "Vorausschauende Instandhaltung" },
  { icon: "◇", label: "Qualität" },
  { icon: "ϟ", label: "Energie" },
  { icon: "◉", label: "OEE & Leistung" },
  { icon: "▤", label: "Aufträge" },
  { icon: "▥", label: "Material & Lager" },
  { icon: "▣", label: "Berichte" },
  { icon: "✦", label: "KI-Erkenntnisse" },
  { icon: "⚙", label: "Einstellungen" },
];

const kpis = demoKpis.map((kpi) => ({
  label: kpi.label,
  value: kpi.value,
  trend: `${kpi.trend > 0 ? "+" : ""}${kpi.trend}%`,
  status: kpi.status === "warning" ? "warning" : "healthy",
}));

const anomalies = demoAnomalies.map((anomaly) => ({
  machine: anomaly.machineId,
  title: anomaly.title,
  value: anomaly.value,
  priority: anomaly.priority,
  time: new Date(anomaly.detectedAt).toLocaleTimeString("de-DE", {
    hour: "2-digit",
    minute: "2-digit",
  }),
}));

const machines = demoMachines.map((machine) => ({
  id: machine.id,
  name: machine.name,
  area: machine.area,
  status: machine.status,
}));

function StatusDot({ status }: { status: string }) {
  return <span className={`status-dot ${status}`} />;
}

function Dashboard({
  onNavigate,
}: {
  onNavigate: (page: Page) => void;
}) {
  return (
    <main className="main-content">
      <header className="topbar">
        <div>
          <div className="eyebrow">LEITSTAND</div>
          <h1>FactoryIQ</h1>
          <p>PCK Schwedt · Pilot Environment</p>
        </div>

        <div className="topbar-actions">
          <button className="ghost-button">⌕ Suche</button>
          <button className="ghost-button">▣ Bericht</button>
          <div className="live-indicator">
            <span />
            LIVE
          </div>
          <div className="user-avatar">TB</div>
        </div>
      </header>

      <section className="hero-row">
        <div>
          <h2>Betriebsübersicht</h2>
          <p>Aktueller Anlagenzustand und industrielle Leistungskennzahlen</p>
        </div>

        <div className="time-selector">
          <button>24 Std.</button>
          <button className="active">7 Tage</button>
          <button>30 Tage</button>
          <button>90 Tage</button>
        </div>
      </section>

      <section className="kpi-grid">
        {kpis.map((kpi) => (
          <button
            className="kpi-card"
            key={kpi.label}
            onClick={() =>
              kpi.label === "OEE"
                ? onNavigate("OEE & Leistung")
                : kpi.label === "Energy"
                  ? onNavigate("Energie")
                  : kpi.label === "Active Alarms"
                    ? onNavigate("Anomalien")
                    : undefined
            }
          >
            <div className="kpi-header">
              <span>{kpi.label}</span>
              <span className={`kpi-status ${kpi.status}`}>
                {kpi.status === "healthy" ? "●" : "●"}
              </span>
            </div>

            <strong>{kpi.value}</strong>

            <div className="kpi-footer">
              <span className={kpi.trend.startsWith("-") ? "positive" : ""}>
                {kpi.trend}
              </span>
              <span>gegenüber vorherigem Zeitraum</span>
            </div>

            <div className="sparkline">
              <i />
              <i />
              <i />
              <i />
              <i />
              <i />
              <i />
            </div>
          </button>
        ))}
      </section>

      <section className="dashboard-grid">
        <div className="panel plant-panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">WERKSÜBERSICHT</span>
              <h3>Werksübersicht</h3>
            </div>
            <button onClick={() => onNavigate("Werksübersicht")}>Details →</button>
          </div>

          <div className="plant-map">
            <div className="plant-zone zone-refinery">
              <span>RAFFINERIE</span>
              <b>P-12</b>
            </div>

            <div className="plant-zone zone-energy">
              <span>ENERGIEZENTRALE</span>
              <b>E-03</b>
            </div>

            <div className="plant-zone zone-supply">
              <span>VERSORGUNG</span>
              <b>K-07</b>
            </div>

            <div className="plant-zone zone-tank">
              <span>TANKLAGER</span>
              <b>T-02</b>
            </div>

            <div className="plant-pipeline pipeline-one" />
            <div className="plant-pipeline pipeline-two" />

            <div className="map-legend">
              <span>
                <StatusDot status="normal" /> Normal
              </span>
              <span>
                <StatusDot status="warning" /> Warnung
              </span>
              <span>
                <StatusDot status="critical" /> Kritisch
              </span>
            </div>
          </div>
        </div>

        <div className="panel anomaly-panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">KI-ÜBERWACHUNG</span>
              <h3>Aktive Anomalien</h3>
            </div>
            <button onClick={() => onNavigate("Anomalien")}>Alle anzeigen →</button>
          </div>

          <div className="anomaly-list">
            {anomalies.map((anomaly) => (
              <button
                className="anomaly-row"
                key={anomaly.machine}
                onClick={() => onNavigate("Anomalien")}
              >
                <div className={`priority ${anomaly.priority.toLowerCase()}`}>
                  {anomaly.priority}
                </div>

                <div className="anomaly-main">
                  <strong>{anomaly.machine}</strong>
                  <span>{anomaly.title}</span>
                </div>

                <div className="anomaly-value">{anomaly.value}</div>
                <time>{anomaly.time}</time>
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="dashboard-grid lower-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">MASCHINENINTELLIGENZ</span>
              <h3>Maschinenstatus</h3>
            </div>
            <button onClick={() => onNavigate("Maschinen")}>Maschinen →</button>
          </div>

          <div className="machine-table">
            {machines.map((machine) => (
              <button
                className="machine-row"
                key={machine.id}
                onClick={() => onNavigate("Maschinen")}
              >
                <StatusDot status={machine.status} />
                <div>
                  <strong>{machine.id}</strong>
                  <span>{machine.name}</span>
                </div>
                <span>{machine.area}</span>
                <b className={`machine-state ${machine.status}`}>
                  {machine.status === "normal"
                    ? "NORMAL"
                    : machine.status === "warning"
                      ? "WARNUNG"
                      : "KRITISCH"}
                </b>
              </button>
            ))}
          </div>
        </div>

        <div className="panel ai-panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">AIHELIXIA ENGINE</span>
              <h3>KI-Erkenntnisse</h3>
            </div>
            <StatusDot status="normal" />
          </div>

          <div className="ai-engine-status">
            <div className="engine-icon">✦</div>
            <div>
              <strong>KI-Engine betriebsbereit</strong>
              <span>Analysedienst verbunden</span>
            </div>
          </div>

          <div className="ai-insight">
            <span>HOHE KONFIDENZ</span>
            <strong>P-12 zeigt ein erhöhtes Ausfallrisiko.</strong>
            <p>
              Vibrationsmuster weichen um 48% vom historischen Normalbereich
              ab.
            </p>
          </div>

          <button
            className="primary-button"
            onClick={() => onNavigate("KI-Erkenntnisse")}
          >
            KI-Analyse öffnen →
          </button>
        </div>
      </section>
    </main>
  );
}

function PlaceholderPage({ page }: { page: Page }) {
  return (
    <main className="main-content">
      <header className="topbar">
        <div>
          <div className="eyebrow">FACTORYIQ LEITSTAND</div>
          <h1>{page}</h1>
          <p>PCK Schwedt · Pilot Environment</p>
        </div>

        <div className="topbar-actions">
          <div className="live-indicator">
            <span />
            LIVE
          </div>
          <div className="user-avatar">TB</div>
        </div>
      </header>

      <section className="placeholder-page">
        <div className="placeholder-icon">◈</div>
        <span className="eyebrow">FACTORYIQ MODUL</span>
        <h2>{page}</h2>
        <p>
          Dieses Modul ist vorbereitet und wird im nächsten Implementierungsschritt
          mit seinen interaktiven Funktionen aufgebaut.
        </p>
      </section>
    </main>
  );
}

export default function App() {
  const [activePage, setActivePage] = useState<Page>("Dashboard");
  const [selectedMachineId, setSelectedMachineId] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className={`app-shell ${sidebarCollapsed ? "collapsed" : ""}`}>
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">F</div>
          <div className="brand-text">
            <strong>FactoryIQ</strong>
            <span>Industrielle Intelligenz</span>
          </div>
        </div>

        <div className="pilot-card">
          <div className="pilot-label">AKTIVER PILOT</div>
          <strong>PCK Schwedt</strong>
          <span>Werk · Schwedt</span>
          <div className="pilot-status">
            <StatusDot status="normal" />
            System betriebsbereit
          </div>
        </div>

        <nav className="navigation">
          {navigation.map((item) => (
            <button
              key={item.label}
              className={activePage === item.label ? "nav-item active" : "nav-item"}
              onClick={() => setActivePage(item.label)}
              title={item.label}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
              {item.label === "Anomalien" && (
                <span className="nav-badge">7</span>
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="system-status">
            <StatusDot status="normal" />
            <div>
              <strong>System Online</strong>
              <span>AIHelixia Engine</span>
            </div>
          </div>

          <div className="sidebar-user">
            <div className="user-avatar">TB</div>
            <div>
              <strong>Administrator</strong>
              <span>AIHelixia</span>
            </div>
          </div>

          <button
            className="collapse-button"
            onClick={() => setSidebarCollapsed((value) => !value)}
          >
            {sidebarCollapsed ? "→" : "←"}
          </button>
        </div>
      </aside>

      <div className="app-content">
        {activePage === "Dashboard" ? (
          <Dashboard onNavigate={setActivePage} />
        ) : activePage === "Maschinen" && selectedMachineId ? (
          <MachineDetail
            machineId={selectedMachineId}
            onBack={() => setSelectedMachineId(null)}
          />
        ) : activePage === "Maschinen" ? (
          <Machines onSelectMachine={setSelectedMachineId} />
        ) : (
          <PlaceholderPage page={activePage} />
        )}
      </div>
    </div>
  );
}
