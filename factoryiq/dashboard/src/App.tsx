import { useEffect, useState } from "react";
import "./App.css";
import Machines from "./pages/Machines";
import { getFactoryDashboard } from "./services/factoryApi";
import MachineDetail from "./pages/MachineDetail";
import Production from "./pages/Production";
import FactoryOverview from "./pages/FactoryOverview";
import Anomalies from "./pages/Anomalies";
import Maintenance from "./pages/Maintenance";
import Quality from "./pages/Quality";
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
  engineDashboard,
  onSelectMachine,
}: {
  onNavigate: (page: Page) => void;
  onSelectMachine: (machineId: string) => void;
  engineDashboard: Awaited<ReturnType<typeof getFactoryDashboard>> | null;
}) {
  const machineStatusSummary = {
    total: machines.length,
    normal: machines.filter((machine) => machine.status === "normal").length,
    warning: machines.filter((machine) => machine.status === "warning").length,
    critical: machines.filter((machine) => machine.status === "critical").length,
  };

  const [dashboardPeriod, setDashboardPeriod] = useState<"24h" | "7d" | "30d" | "90d">("7d");
  const dashboardKpis = kpis.map((kpi) => {
    if (kpi.label === "Active Alarms" && engineDashboard) {
      return {
        ...kpi,
        value: String(engineDashboard.kpis.alarm_count),
      };
    }

    if (kpi.label === "Machines" && engineDashboard) {
      return {
        ...kpi,
        value: String(engineDashboard.kpis.machine_count),
      };
    }

    if (kpi.label === "Energy" && engineDashboard) {
      return {
        ...kpi,
        value: `${engineDashboard.kpis.energy_consumption ?? "—"} ${
          engineDashboard.kpis.energy_unit ?? ""
        }`.trim(),
      };
    }

    if (kpi.label === "Production" && engineDashboard) {
      return {
        ...kpi,
        value: String(engineDashboard.kpis.production_output ?? "—"),
      };
    }

    return kpi;
  });

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
          <button className={dashboardPeriod === "24h" ? "active" : ""} onClick={() => setDashboardPeriod("24h")}>24 Std.</button>
          <button className={dashboardPeriod === "7d" ? "active" : ""} onClick={() => setDashboardPeriod("7d")}>7 Tage</button>
          <button className={dashboardPeriod === "30d" ? "active" : ""} onClick={() => setDashboardPeriod("30d")}>30 Tage</button>
          <button className={dashboardPeriod === "90d" ? "active" : ""} onClick={() => setDashboardPeriod("90d")}>90 Tage</button>
        </div>
      </section>

      <section className="kpi-grid">
        {dashboardKpis.map((kpi) => (
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
              <span className={Number(kpi.trend) < 0 ? "positive" : ""}>
                {Number(kpi.trend) > 0 ? "+" : ""}{Number(kpi.trend).toFixed(1).replace(".", ",")} %
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
            <button className="plant-zone zone-refinery" onClick={() => { onSelectMachine("P-12"); onNavigate("Maschinen"); }}>
              <span>RAFFINERIE</span>
              <b>P-12 · R-101</b>
            </button>

            <button className="plant-zone zone-energy" onClick={() => { onSelectMachine("E-03"); onNavigate("Maschinen"); }}>
              <span>ENERGIEZENTRALE</span>
              <b>E-03 · F-01</b>
            </button>

            <button className="plant-zone zone-supply" onClick={() => { onSelectMachine("K-07"); onNavigate("Maschinen"); }}>
              <span>VERSORGUNG</span>
              <b>K-07</b>
            </button>

            <button className="plant-zone zone-tank" onClick={() => { onSelectMachine("T-02"); onNavigate("Maschinen"); }}>
              <span>TANKLAGER</span>
              <b>T-02</b>
            </button>

            <button className="plant-zone zone-maintenance" onClick={() => { onSelectMachine("M-05"); onNavigate("Maschinen"); }}>
              <span>INSTANDHALTUNG</span>
              <b>M-05</b>
            </button>

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
            {anomalies.slice(0, 5).map((anomaly) => (
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

          <div className="machine-status-summary">
            <div><span className="status-dot normal" /><strong>{machineStatusSummary.normal}</strong><small>Normal</small></div>
            <div><span className="status-dot warning" /><strong>{machineStatusSummary.warning}</strong><small>Warnung</small></div>
            <div><span className="status-dot critical" /><strong>{machineStatusSummary.critical}</strong><small>Kritisch</small></div>
            <div className="machine-status-total"><strong>{machineStatusSummary.total}</strong><small>Gesamt</small></div>
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
            <StatusDot status={engineDashboard ? "normal" : "critical"} />
          </div>

          <div className="ai-engine-status">
            <div className="engine-icon">✦</div>
            <div>
              <strong>
                {engineDashboard
                  ? "KI-Engine betriebsbereit"
                  : "KI-Engine offline"}
              </strong>
              <span>
                {engineDashboard
                  ? "Analysedienst verbunden · ONLINE"
                  : "Demo-Daten aktiv · OFFLINE"}
              </span>
            </div>
          </div>

          <div className="ai-insight">
            <span>{anomalies[0]?.priority ?? "INFO"} · KI-ERKENNTNIS</span>
            <strong>
              {anomalies[0]?.machine ?? "Keine Maschine"} zeigt ein auffälliges Muster.
            </strong>
            <p>
              {anomalies[0]?.title ?? "Aktuell liegen keine relevanten Anomalien vor."}
              {anomalies[0]?.value ? ` · Messwert ${anomalies[0].value}` : ""}
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
  const [engineDashboard, setEngineDashboard] = useState<Awaited<
    ReturnType<typeof getFactoryDashboard>
  > | null>(null);

  useEffect(() => {
    getFactoryDashboard()
      .then((data) => {
        console.log("[FactoryIQ] Engine Dashboard verbunden:", data);
        setEngineDashboard(data);
      })
      .catch((error) => {
        console.warn("[FactoryIQ] Engine nicht erreichbar:", error);
      });
  }, []);

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
          <Dashboard
            onNavigate={setActivePage}
            onSelectMachine={setSelectedMachineId}
            engineDashboard={engineDashboard}
          />
        ) : activePage === "Maschinen" && selectedMachineId ? (
          <MachineDetail
            machineId={selectedMachineId}
            onBack={() => setSelectedMachineId(null)}
            engineDashboard={engineDashboard}
          />
        ) : activePage === "Maschinen" ? (
          <Machines onSelectMachine={setSelectedMachineId} engineDashboard={engineDashboard} />
        ) : activePage === "Produktion" ? (
          <Production
            engineDashboard={engineDashboard}
            onBack={() => setActivePage("Dashboard")}
          />
        ) : activePage === "Werksübersicht" ? (
          <FactoryOverview
            engineDashboard={engineDashboard}
            onBack={() => setActivePage("Dashboard")}
          />
        ) : activePage === "Anomalien" ? (
          <Anomalies
            engineDashboard={engineDashboard}
            onBack={() => setActivePage("Dashboard")}
          />
        ) : activePage === "Vorausschauende Instandhaltung" ? (
          <Maintenance
            engineDashboard={engineDashboard}
            onBack={() => setActivePage("Dashboard")}
          />
        ) : activePage === "Qualität" ? (
          <Quality
            engineDashboard={engineDashboard}
            onBack={() => setActivePage("Dashboard")}
          />
        ) : (
          <PlaceholderPage page={activePage} />
        )}
      </div>
    </div>
  );
}
