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

type IntelligenceData = {
  reasoning?: any;
  prediction?: any;
  decision?: any;
  evaluation?: any;
  feedback?: any;
  aiResults?: any;
}

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
      action: string;
      priority: string;
      reason: string;
      machine_ids?: string[];
    };
    prediction: {
      version?: string;
      status?: string;
      prediction_id?: number;
      scenario_count?: number;
      scenarios?: Array<{
        type?: string;
        source?: string;
        machine_id?: string;
        priority?: string;
        confidence?: string;
        severity?: string;
        description?: string;
        trigger_signals?: string[];
        evidence?: {
          evidence_count?: number;
          supporting_signals?: string[];
          correlated_machines?: string[];
          evidence_strength?: string;
        };
      }>;
      evidence_summary?: {
        scenario_count?: number;
        total_evidence_count?: number;
        strong_evidence_scenarios?: number;
        moderate_evidence_scenarios?: number;
        limited_evidence_scenarios?: number;
        no_evidence_scenarios?: number;
        confidence_levels?: Record<string, number>;
        historical_support?: {
          status?: string;
          known_outcome_count?: number;
          average_confidence?: number | null;
          dominant_outcome?: string | null;
          success_rate?: number | null;
          improved_count?: number;
          degraded_count?: number;
          unchanged_count?: number;
        };
        historical_supported_scenarios?: number;
      };
      historical_support?: {
        status?: string;
        known_outcome_count?: number;
        average_confidence?: number | null;
        dominant_outcome?: string | null;
        success_rate?: number | null;
        improved_count?: number;
        degraded_count?: number;
        unchanged_count?: number;
      };
    };
    decision: {
      status: string;
      decision_type: string;
      action: string;
      rationale: string;
      scenario_count: number;
      root_cause?: {
        status?: string;
        hypothesis_count?: number;
        primary_type?: string;
        priority?: string;
        confidence?: string;
      };
      evidence?: {
        evidence_count?: number;
        evidence_strength?: string;
        supporting_signals?: string[];
        correlated_machines?: string[];
        supporting_predictions?: string[];
        historical_support?: {
          status?: string;
          strength?: string;
          known_outcome_count?: number;
          average_confidence?: number | null;
          dominant_outcome?: string | null;
        };
      };
    };
    evaluation: {
      status: string;
      evaluation: string;
      score: number;
      message: string;
      action_status: string;
      execution_evaluation?: string;
      execution_score?: number;
      outcome_status?: string;
      outcome_evaluation?: string;
      outcome_score?: number | null;
      outcome_confidence?: number;
      outcome_known?: boolean;
      outcome_result_available?: boolean;
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


function formatLabel(value: string) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function App() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [intelligence, setIntelligence] = useState<IntelligenceData | null>(null);
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState("Dashboard");

  const getWeatherLabel = (code: number | null) => {
    if (code === null) return "Wetter wird geladen";
    if (code === 0) return "Klar";
    if ([1, 2].includes(code)) return "Teilweise bewölkt";
    if (code === 3) return "Bedeckt";
    if ([45, 48].includes(code)) return "Nebel";
    if ([51, 53, 55, 56, 57].includes(code)) return "Nieselregen";
    if ([61, 63, 65, 66, 67].includes(code)) return "Regen";
    if ([71, 73, 75, 77].includes(code)) return "Schnee";
    if ([80, 81, 82].includes(code)) return "Regenschauer";
    if ([85, 86].includes(code)) return "Schneeschauer";
    if ([95, 96, 99].includes(code)) return "Gewitter";
    return "Aktuelle Bedingungen";
  };

  const getWeatherIcon = (code: number | null) => {
    if (code === null) return "·";
    if (code === 0) return "☀";
    if ([1, 2].includes(code)) return "◐";
    if (code === 3) return "☁";
    if ([45, 48].includes(code)) return "≋";
    if ([51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return "☂";
    if ([71, 73, 75, 77, 85, 86].includes(code)) return "❄";
    if ([95, 96, 99].includes(code)) return "ϟ";
    return "◌";
  };


  const [currentTime, setCurrentTime] = useState(new Date());

  const [readAlarmIds, setReadAlarmIds] = useState<string[]>([]);

  const unreadAlarmCount = data
    ? data.alarms.alarms.filter(
        (alarm) => !readAlarmIds.includes(alarm.id)
      ).length
    : 0;




  const [showSystemPanel, setShowSystemPanel] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      const target = event.target as HTMLElement;

      const insideSystem =
        !!target.closest(".topbar-system") ||
        !!target.closest(".system-status-button") ||
        !!target.closest(".system-popover");

      const insideNotifications =
        !!target.closest(".notification-button") ||
        !!target.closest(".notification-popover");

      const insideUser =
        !!target.closest(".user-menu-wrapper") ||
        !!target.closest(".user-avatar-button") ||
        !!target.closest(".user-popover");

      if (!insideSystem) {
        setShowSystemPanel(false);
      }

      if (!insideNotifications) {
        setShowNotifications(false);
      }

      if (!insideUser) {
        setShowUserMenu(false);
      }

      if (!target.closest(".time-range-control")) {
        setShowTimeRangeMenu(false);
      }

      if (!target.closest(".command-menu-control")) {
        setShowCommandMenu(false);
      }
    };

    document.addEventListener("click", handleOutsideClick);

    return () => {
      document.removeEventListener("click", handleOutsideClick);
    };
  }, []);

  const [showUserMenu, setShowUserMenu] = useState(false);


  const [weather, setWeather] = useState<{
    temperature: number | null;
    humidity: number | null;
    windSpeed: number | null;
    weatherCode: number | null;
  }>({
    temperature: null,
    humidity: null,
    windSpeed: null,
    weatherCode: null,
  });


  useEffect(() => {
    const timer = window.setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => window.clearInterval(timer);
  }, []);
useEffect(() => {
    let cancelled = false;

    const loadWeather = async () => {
      try {
        const response = await fetch(
          "https://api.open-meteo.com/v1/forecast?latitude=53.0596&longitude=14.2815&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&temperature_unit=celsius&wind_speed_unit=kmh&timezone=Europe%2FBerlin"
        );

        if (!response.ok) {
          throw new Error(`Weather API ${response.status}`);
        }

        const payload = await response.json();

        if (cancelled) {
          return;
        }

        setWeather({
          temperature: payload.current?.temperature_2m ?? null,
          humidity: payload.current?.relative_humidity_2m ?? null,
          windSpeed: payload.current?.wind_speed_10m ?? null,
          weatherCode: payload.current?.weather_code ?? null,
        });
      } catch (error) {
        console.error("FactoryIQ weather error:", error);
      }
    };

    loadWeather();

    const weatherTimer = window.setInterval(loadWeather, 10 * 60 * 1000);

    return () => {
      cancelled = true;
      window.clearInterval(weatherTimer);
    };
  }, []);


  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [selectedTimeRange, setSelectedTimeRange] = useState("Letzte 24 Stunden");
  const [showTimeRangeMenu, setShowTimeRangeMenu] = useState(false);
  const [showCommandMenu, setShowCommandMenu] = useState(false);

  async function loadDashboard() {
    try {
      const response = await fetch("/api/factory/dashboard");

      if (!response.ok) {
        const body = await response.text();
        throw new Error(body || `HTTP ${response.status}`);
      }

      const dashboard = await response.json();
      setData(dashboard);

    try {
      const intelligenceResponse = await fetch("/api/factory/intelligence");

      if (intelligenceResponse.ok) {
        const intelligenceData = await intelligenceResponse.json();

        try {
          const aiResultsResponse = await fetch("/api/ai-results");

          if (aiResultsResponse.ok) {
            const aiResultsData = await aiResultsResponse.json();

            setIntelligence({
              ...intelligenceData,
              aiResults: aiResultsData,
            });
          } else {
            setIntelligence(intelligenceData);
          }
        } catch {
          setIntelligence(intelligenceData);
        }
      }
    } catch {
      // Intelligence darf den Dashboard-Load nicht blockieren.
    }
      setError("");
      setLastUpdate(new Date());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Dashboard konnte nicht geladen werden.");
    }
  }

  useEffect(() => {
    loadDashboard();

    const dashboardTimer = window.setInterval(() => {
      loadDashboard();
    }, 15000);

    return () => {
      window.clearInterval(dashboardTimer);
    };
  }, []);


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

  const exportFactoryIQSnapshot = () => {
    const snapshot = {
      exported_at: new Date().toISOString(),
      last_dashboard_sync: lastUpdate.toISOString(),
      time_range: selectedTimeRange,
      factory: data.factory,
      kpis: data.kpis,
      machines: data.machines,
      alarms: data.alarms,
      production: data.production,
      energy: data.energy,
      maintenance: data.maintenance,
      ai: data.ai,
      historical_patterns: data.historical_patterns,
    };

    const blob = new Blob(
      [JSON.stringify(snapshot, null, 2)],
      { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = `factoryiq-snapshot-${new Date()
      .toISOString()
      .replace(/[:.]/g, "-")}.json`;

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
  };

  const activeMachine = data.machines.machines[0];

  const alarmCount = data.kpis.alarm_count;
  const criticalCount = data.alarms.severity_counts.critical ?? 0;
  const warningCount = data.alarms.severity_counts.warning ?? 0;
  const runningMachines = data.machines.status_counts.running ?? 0;
  const machineCount = data.kpis.machine_count;
  const productionTarget = Number(data.kpis.production_target ?? 0);
  const productionOutput = Number(data.kpis.production_output ?? 0);
  const decisionType = data.ai.decision?.decision_type ?? "review";

  const learningAction = data.ai.learning_signal?.action ?? "review";
  const learningReason = data.ai.learning_signal?.reason ?? "Kein Learning-Signal verfügbar.";
  const predictionScenarios = data.ai.prediction?.scenarios ?? [];
  const primaryPrediction =
    predictionScenarios.find((scenario) => scenario.priority === "high") ??
    predictionScenarios[0];

  const predictionTitle = primaryPrediction?.type
    ? formatLabel(primaryPrediction.type)
    : "Keine Prediction verfügbar";

  const predictionDescription =
    primaryPrediction?.description ??
    "Die Intelligence Engine hat aktuell keine weiterführende Prediction bereitgestellt.";

  const predictionSeverity =
    primaryPrediction?.severity ??
    primaryPrediction?.priority ??
    "normal";

  const predictionEvidence =
    primaryPrediction?.evidence?.evidence_count ??
    0;

  const predictionSignals =
    primaryPrediction?.trigger_signals ??
    primaryPrediction?.evidence?.supporting_signals ??
    [];

  const decisionAction = data.ai.decision?.action ?? "observe";
  const decisionRationale =
    data.ai.decision?.rationale ??
    "Keine Entscheidungsbegründung verfügbar.";

  const evaluationStatus =
    data.ai.evaluation?.evaluation ??
    "unknown";

  const evaluationScore =
    Number(data.ai.evaluation?.score ?? 0);

  const machine = data.machines.machines[0];

  const machinePrediction =
    predictionScenarios.find(
      (scenario) =>
        scenario.machine_id === machine?.id &&
        scenario.type === "potential_machine_degradation",
    ) ??
    predictionScenarios.find(
      (scenario) => scenario.machine_id === machine?.id,
    );

  const machineEvidenceCount =
    machinePrediction?.evidence?.evidence_count ??
    predictionEvidence;

  const machineEvidenceStrength =
    machinePrediction?.evidence?.evidence_strength ??
    "unknown";

  const machineSignals =
    machinePrediction?.trigger_signals ??
    predictionSignals;

  const machineSeverity =
    machinePrediction?.severity ??
    predictionSeverity;

  const machineConfidence =
    machinePrediction?.confidence ??
    "unknown";

  const machineStatus =
    machine?.status ??
    "unknown";

  const aiResults =
    intelligence?.aiResults ?? {};

  const resultRecords =
    Array.isArray(aiResults?.records)
      ? aiResults.records
      : Array.isArray(aiResults)
        ? aiResults
        : [];

  const reasoningRecord =
    resultRecords.find(
      (record: any) =>
        record?.result_type === "reasoning",
    ) ?? {};

  const reasoningData =
    reasoningRecord?.data ??
    {};

  const industrialAnalysis =
    reasoningData?.industrial_analysis ??
    {};

  const anomalyAnalysis =
    industrialAnalysis?.anomaly_analysis ??
    reasoningData?.anomaly_analysis ??
    {};

  const anomalySignals =
    Array.isArray(anomalyAnalysis?.signals)
      ? anomalyAnalysis.signals
      : [];

  const vibrationSignal =
    anomalySignals.find(
      (signal: any) =>
        signal?.signal === "vibration_elevated" ||
        signal?.type === "vibration_elevated",
    ) ?? null;

  const vibrationValue =
    typeof vibrationSignal?.value === "number"
      ? vibrationSignal.value
      : null;

  const vibrationUnit =
    vibrationSignal?.unit ?? "mm/s";

  const vibrationThreshold =
    typeof vibrationSignal?.threshold === "number"
      ? vibrationSignal.threshold
      : null;

  const anomalyConfidence =
    typeof anomalyAnalysis?.confidence === "number"
      ? anomalyAnalysis.confidence
      : null;

  const anomalySeverity =
    anomalyAnalysis?.severity ??
    machineSeverity;

  const anomalySignalCount =
    typeof anomalyAnalysis?.signal_count === "number"
      ? anomalyAnalysis.signal_count
      : anomalySignals.length;

  const vibrationExcessPercent =
    vibrationValue !== null &&
    vibrationThreshold !== null &&
    vibrationThreshold > 0
      ? ((vibrationValue - vibrationThreshold) / vibrationThreshold) * 100
      : null;

  const vibrationGaugePercent =
    vibrationValue !== null &&
    vibrationThreshold !== null &&
    vibrationThreshold > 0
      ? Math.min((vibrationValue / vibrationThreshold) * 50, 100)
      : 0;

  const primaryIncident =
    data?.alarms?.alarms?.find(
      (alarm: any) => alarm?.severity === "critical",
    ) ??
    data?.alarms?.alarms?.[0] ??
    null;

  const historicalPatterns =
    data?.historical_patterns ?? {};

  const historicalEntryCount =
    typeof historicalPatterns?.entry_count === "number"
      ? historicalPatterns.entry_count
      : 0;

  const recurringMachineIds =
    Array.isArray(historicalPatterns?.recurring_machine_ids)
      ? historicalPatterns.recurring_machine_ids
      : [];

  const historicalMachineCounts =
    historicalPatterns?.machine_counts ?? {};

  const historicalStatusCounts =
    historicalPatterns?.status_counts ?? {};

  const historicalRunning =
    typeof historicalStatusCounts?.running === "number"
      ? historicalStatusCounts.running
      : 0;

  const historicalWarning =
    typeof historicalStatusCounts?.warning === "number"
      ? historicalStatusCounts.warning
      : 0;

  const historicalRunningRate =
    historicalEntryCount > 0
      ? (historicalRunning / historicalEntryCount) * 100
      : 0;

  const operationalTimeline = [
    {
      stage: "Signal",
      status:
        vibrationValue !== null
          ? "Vibration Elevated"
          : "Critical Alarm",
      detail:
        vibrationValue !== null && vibrationThreshold !== null
          ? `${vibrationValue.toFixed(1)} ${vibrationUnit} > ${vibrationThreshold.toFixed(1)} ${vibrationUnit}`
          : machineSignals.map(formatLabel).join(" · "),
    },
    {
      stage: "Anomaly",
      status: formatLabel(anomalySeverity),
      detail: `${anomalySignalCount} korrelierte Signale erkannt`,
    },
    {
      stage: "Prediction",
      status: predictionTitle,
      detail:
        machineConfidence !== "unknown"
          ? `Confidence: ${formatLabel(machineConfidence)}`
          : predictionDescription,
    },
    {
      stage: "Evidence",
      status: formatLabel(machineEvidenceStrength),
      detail: `${machineEvidenceCount} Evidence Items`,
    },
    {
      stage: "Decision",
      status: formatLabel(decisionType),
      detail: `→ ${formatLabel(decisionAction)}`,
    },
    {
      stage: "Evaluation",
      status: formatLabel(evaluationStatus),
      detail: `Score ${evaluationScore.toFixed(2)}`,
    },
    {
      stage: "Learning",
      status: formatLabel(learningAction),
      detail: learningReason,
    },
  ];

  if (activeSection === "Einstellungen") {
    return (
      <main className="settings-page">
        <div className="settings-header">
          <div>
            <div className="settings-eyebrow">SYSTEM CONFIGURATION</div>
            <h1>Einstellungen</h1>
            <p>
              FactoryIQ System-, Engine- und Dashboard-Konfiguration.
            </p>
          </div>

          <div className="settings-status-badge">
            <span className="settings-status-dot online" />
            System Online
          </div>
        </div>

        <section className="settings-grid">

          <article className="settings-card">
            <div className="settings-card-header">
              <div>
                <span className="settings-label">ENGINE</span>
                <h2>AIHelixia Intelligence Engine</h2>
              </div>
              <span className="settings-pill success">ONLINE</span>
            </div>

            <div className="settings-list">
              <div className="settings-row">
                <span>Engine Status</span>
                <strong>Online</strong>
              </div>
              <div className="settings-row">
                <span>Engine Version</span>
                <strong>{data.version || "0.1.0"}</strong>
              </div>
              <div className="settings-row">
                <span>Decision Engine</span>
                <strong>0.5.1</strong>
              </div>
              <div className="settings-row">
                <span>Prediction Engine</span>
                <strong>0.9.1</strong>
              </div>
              <div className="settings-row">
                <span>Evaluation Engine</span>
                <strong>0.4.0</strong>
              </div>
            </div>
          </article>

          <article className="settings-card">
            <div className="settings-card-header">
              <div>
                <span className="settings-label">FACTORY</span>
                <h2>Standortkonfiguration</h2>
              </div>
              <span className="settings-pill">ACTIVE</span>
            </div>

            <div className="settings-list">
              <div className="settings-row">
                <span>Factory ID</span>
                <strong>{data.factory.id}</strong>
              </div>
              <div className="settings-row">
                <span>Standort</span>
                <strong>{data.factory.location}</strong>
              </div>
              <div className="settings-row">
                <span>Status</span>
                <strong>{data.factory.status}</strong>
              </div>
              <div className="settings-row">
                <span>Maschinen</span>
                <strong>{data.kpis.machine_count}</strong>
              </div>
              <div className="settings-row">
                <span>Produktionslinien</span>
                <strong>1</strong>
              </div>
            </div>
          </article>

          <article className="settings-card">
            <div className="settings-card-header">
              <div>
                <span className="settings-label">INTELLIGENCE</span>
                <h2>KI-Konfiguration</h2>
              </div>
              <span className="settings-pill success">ACTIVE</span>
            </div>

            <div className="settings-list">
              <div className="settings-row">
                <span>Prediction</span>
                <strong>Aktiv</strong>
              </div>
              <div className="settings-row">
                <span>Anomaly Detection</span>
                <strong>Aktiv</strong>
              </div>
              <div className="settings-row">
                <span>Root Cause Analysis</span>
                <strong>Aktiv</strong>
              </div>
              <div className="settings-row">
                <span>Decision Engine</span>
                <strong>Aktiv</strong>
              </div>
              <div className="settings-row">
                <span>Learning Loop</span>
                <strong>Aktiv</strong>
              </div>
            </div>
          </article>

          <article className="settings-card">
            <div className="settings-card-header">
              <div>
                <span className="settings-label">DATA</span>
                <h2>Datenquellen</h2>
              </div>
              <span className="settings-pill">CONNECTED</span>
            </div>

            <div className="settings-list">
              <div className="settings-row">
                <span>Factory Data</span>
                <strong>Connected</strong>
              </div>
              <div className="settings-row">
                <span>Machine Signals</span>
                <strong>Available</strong>
              </div>
              <div className="settings-row">
                <span>Alarm History</span>
                <strong>{data.kpis.alarm_count} Alarme</strong>
              </div>
              <div className="settings-row">
                <span>AI Results</span>
                <strong>Available</strong>
              </div>
              <div className="settings-row">
                <span>Historical Patterns</span>
                <strong>{data.historical_patterns.entry_count} Entries</strong>
              </div>
            </div>
          </article>

        </section>

        <section className="module-card settings-security">
          <div className="settings-card-header">
            <div>
              <span className="settings-label">SYSTEM</span>
              <h2>Systemstatus</h2>
            </div>
            <span className="settings-pill success">HEALTHY</span>
          </div>

          <div className="system-health-grid">
            <div>
              <span>API</span>
              <strong>Operational</strong>
            </div>
            <div>
              <span>Database</span>
              <strong>Operational</strong>
            </div>
            <div>
              <span>AI Pipeline</span>
              <strong>Operational</strong>
            </div>
            <div>
              <span>Dashboard</span>
              <strong>Operational</strong>
            </div>
          </div>
        </section>
      </main>
    );
  }


  return (
    <div className="app-shell">
      {activeSection !== "Dashboard" && (
          <div className="factoryiq-module-overlay">
            {activeSection === "Werke" ? (
              <section className="factoryiq-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">FACTORYIQ MODULE</span>
                    <h1>Werke</h1>
                    <p>Werksübergreifende Transparenz der verbundenen Produktionsumgebung.</p>
                  </div>
                  <span className="module-live-badge">Engine Connected</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>Werk</span>
                    <strong>{data.factory.name}</strong>
                  </div>
                  <div className="module-kpi">
                    <span>Standort</span>
                    <strong>{data.factory.location}</strong>
                  </div>
                  <div className="module-kpi">
                    <span>Maschinen</span>
                    <strong>{data.kpis.machine_count}</strong>
                  </div>
                  <div className="module-kpi">
                    <span>Aktive Alarme</span>
                    <strong>{data.kpis.alarm_count}</strong>
                  </div>
                </div>

                <div className="plant-detail-grid">
                  <div className="plant-detail-card">
                    <div className="plant-card-header">
                      <div>
                        <span className="section-eyebrow">CONNECTED PLANT</span>
                        <h2>{data.factory.name}</h2>
                      </div>
                      <span className="plant-online-badge">● Online</span>
                    </div>

                    <div className="plant-location">
                      <span>Standort</span>
                      <strong>{data.factory.location}</strong>
                    </div>

                    <div className="plant-operation">
                      <span>Betriebsstatus</span>
                      <strong>{data.factory.status}</strong>
                    </div>
                  </div>

                  <div className="plant-detail-card">
                    <span className="section-eyebrow">OPERATIONS</span>
                    <div className="module-stat-row">
                      <span>Produktion</span>
                      <strong>{data.kpis.production_output} / {data.kpis.production_target}</strong>
                    </div>
                    <div className="module-stat-row">
                      <span>Energie</span>
                      <strong>{data.kpis.energy_consumption} {data.kpis.energy_unit}</strong>
                    </div>
                    <div className="module-stat-row">
                      <span>Running Machines</span>
                      <strong>{data.machines.status_counts.running ?? 0} / {data.kpis.machine_count}</strong>
                    </div>
                    <div className="module-stat-row">
                      <span>Operational Signal</span>
                      <strong>{formatLabel(data.ai.operational_signal)}</strong>
                    </div>
                  </div>
                </div>
              </section>
            ) : activeSection === "Produktion" ? (
              <section className="factoryiq-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">PRODUCTION INTELLIGENCE</span>
                    <h1>Produktion</h1>
                    <p>Produktionsleistung und aktueller operativer Zustand des verbundenen Werks.</p>
                  </div>
                  <span className="module-live-badge">Live Production Data</span>
                </div>

                <div className="module-kpis production-kpis">
                  <div className="module-kpi">
                    <span>Output</span>
                    <strong>{productionOutput}</strong>
                    <small>aktueller Produktionsoutput</small>
                  </div>
                  <div className="module-kpi">
                    <span>Target</span>
                    <strong>{productionTarget}</strong>
                    <small>Produktionsziel</small>
                  </div>
                  <div className="module-kpi">
                    <span>Zielerreichung</span>
                    <strong>{productionTarget > 0 ? `${Math.round((productionOutput / productionTarget) * 100)}%` : "—"}</strong>
                    <small>Output vs. Target</small>
                  </div>
                  <div className="module-kpi">
                    <span>Status</span>
                    <strong>Running</strong>
                    <small>aktueller Betriebszustand</small>
                  </div>
                </div>

                <div className="production-grid">
                  <div className="production-main-card">
                    <span className="section-eyebrow">PRODUCTION PERFORMANCE</span>
                    <h2>Produktionsleistung</h2>

                    <div className="production-progress">
                      <div className="production-progress-header">
                        <span>Output vs. Target</span>
                        <strong>{productionOutput} / {productionTarget}</strong>
                      </div>
                      <div className="production-progress-track">
                        <div
                          className="production-progress-fill"
                          style={{
                            width: `${Math.min(
                              100,
                              productionTarget > 0
                                ? (productionOutput / productionTarget) * 100
                                : 0
                            )}%`,
                          }}
                        />
                      </div>
                      <div className="production-progress-scale">
                        <span>0</span>
                        <span>Target</span>
                      </div>
                    </div>

                    <div className="production-status-box">
                      <span>PRODUCTION STATUS</span>
                      <strong>Running</strong>
                      <small>Die Produktionsleistung wird direkt aus dem FactoryIQ Operational Snapshot übernommen.</small>
                    </div>
                  </div>

                  <div className="production-main-card">
                    <span className="section-eyebrow">OPERATIONAL CONTEXT</span>
                    <h2>Produktionsumfeld</h2>

                    <div className="module-stat-row">
                      <span>Aktive Maschinen</span>
                      <strong>{runningMachines} / {machineCount}</strong>
                    </div>
                    <div className="module-stat-row">
                      <span>Energieverbrauch</span>
                      <strong>{data.kpis.energy_consumption} {data.kpis.energy_unit}</strong>
                    </div>
                    <div className="module-stat-row">
                      <span>Aktive Alarme</span>
                      <strong>{alarmCount}</strong>
                    </div>
                    <div className="module-stat-row">
                      <span>Kritische Alarme</span>
                      <strong>{criticalCount}</strong>
                    </div>
                    <div className="module-stat-row">
                      <span>AI Signal</span>
                      <strong>{formatLabel(data.ai.operational_signal)}</strong>
                    </div>
                  </div>
                </div>
              </section>
            ) : activeSection === "Maschinen" ? (
              <section className="factoryiq-module machine-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">MACHINE INTELLIGENCE</span>
                    <h1>Maschinen</h1>
                    <p>Zustand, Anomalien und AI-Bewertung der verbundenen Maschinen.</p>
                  </div>
                  <span className="module-live-badge">Engine Connected</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>Gesamt</span>
                    <strong>{machineCount}</strong>
                    <small>verbundene Maschinen</small>
                  </div>
                  <div className="module-kpi">
                    <span>Running</span>
                    <strong>{runningMachines}</strong>
                    <small>aktiver Betrieb</small>
                  </div>
                  <div className="module-kpi">
                    <span>Warning</span>
                    <strong>{data.machines.status_counts.warning ?? 0}</strong>
                    <small>Warnstatus</small>
                  </div>
                  <div className="module-kpi">
                    <span>Critical</span>
                    <strong>{criticalCount}</strong>
                    <small>kritische Signale</small>
                  </div>
                </div>

                <div className="machine-intelligence-layout">
                  <div className="machine-list-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">CONNECTED MACHINES</span>
                        <h2>Maschinenübersicht</h2>
                      </div>
                      <span className="machine-count-badge">{machineCount} connected</span>
                    </div>

                    <div className="machine-list">
                      {data.machines.machines.map((machine) => {
                        const machineHasRisk =
                          anomalySeverity.toLowerCase() === "high" &&
                          machine.id === data.machines.machines[0]?.id;

                        return (
                          <div className="machine-row" key={machine.id}>
                            <div className="machine-identity">
                              <div className={`machine-status-dot ${machine.status.toLowerCase()}`} />
                              <div>
                                <strong>{machine.name}</strong>
                                <span>{machine.id}</span>
                              </div>
                            </div>

                            <div className="machine-line">
                              <span>Production Line</span>
                              <strong>{machine.production_line_id}</strong>
                            </div>

                            <div className="machine-state">
                              <span>Status</span>
                              <strong>{formatLabel(machine.status)}</strong>
                            </div>

                            <div className={`machine-risk ${machineHasRisk ? "high" : "normal"}`}>
                              {machineHasRisk ? "AI Risk High" : "Normal"}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  <div className="machine-detail-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">MACHINE ASSESSMENT</span>
                        <h2>{activeMachine?.id ?? "MACHINE-001"}</h2>
                      </div>
                      <span className={`machine-risk-badge ${anomalySeverity.toLowerCase()}`}>
                        {formatLabel(anomalySeverity)}
                      </span>
                    </div>

                    <div className="machine-detail-grid">
                      <div className="machine-detail-metric">
                        <span>Vibration</span>
                        <strong>{vibrationValue} {vibrationUnit}</strong>
                        <small>Threshold {vibrationThreshold} {vibrationUnit}</small>
                      </div>

                      <div className="machine-detail-metric">
                        <span>Anomaly</span>
                        <strong>{formatLabel(anomalySeverity)}</strong>
                        <small>{predictionSignals.length} correlated signals</small>
                      </div>

                      <div className="machine-detail-metric">
                        <span>Confidence</span>
                        <strong>{Math.round(anomalyConfidence * 100)}%</strong>
                        <small>AI anomaly confidence</small>
                      </div>

                      <div className="machine-detail-metric">
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                        <small>supporting evidence items</small>
                      </div>
                    </div>

                    <div className="machine-signal-panel">
                      <span className="section-eyebrow">ACTIVE SIGNALS</span>
                      <div className="signal-chip-row">
                        {predictionSignals.length > 0 ? (
                          predictionSignals.map((signal) => (
                            <span className="signal-chip" key={signal}>
                              {formatLabel(signal)}
                            </span>
                          ))
                        ) : (
                          <span className="signal-chip">No active signal</span>
                        )}
                      </div>
                    </div>

                    <div className="machine-ai-assessment">
                      <div>
                        <span className="section-eyebrow">AI PREDICTION</span>
                        <strong>{predictionTitle}</strong>
                        <p>{predictionDescription}</p>
                      </div>

                      <div className="machine-ai-decision">
                        <span>Decision</span>
                        <strong>{formatLabel(decisionType)} → {formatLabel(decisionAction)}</strong>
                        <small>{decisionRationale}</small>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="machine-history-card">
                  <div className="machine-card-heading">
                    <div>
                      <span className="section-eyebrow">HISTORICAL INTELLIGENCE</span>
                      <h2>Machine History</h2>
                    </div>
                    <span className="machine-count-badge">
                      {data.historical_patterns.entry_count} observations
                    </span>
                  </div>

                  <div className="machine-history-grid">
                    <div className="history-metric">
                      <span>Machine</span>
                      <strong>{activeMachine?.id ?? "—"}</strong>
                      <small>{data.historical_patterns.entry_count} historical observations</small>
                    </div>

                    <div className="history-metric">
                      <span>Running History</span>
                      <strong>
                        {data.historical_patterns.entry_count > 0
                          ? `${Math.round(((data.historical_patterns.status_counts.running ?? 0) / data.historical_patterns.entry_count) * 100)}%`
                          : "—"}
                      </strong>
                      <small>{data.historical_patterns.status_counts.running ?? 0} observations</small>
                    </div>

                    <div className="history-metric">
                      <span>Warning History</span>
                      <strong>{data.historical_patterns.status_counts.warning ?? 0}</strong>
                      <small>recorded observations</small>
                    </div>

                    <div className="history-metric">
                      <span>Signal Density</span>
                      <strong>{data.historical_patterns.recurring_machine_ids.length}</strong>
                      <small>machine(s) represented in history</small>
                    </div>
                  </div>
                </div>
              </section>
            ) : activeSection === "Anomalien" ? (
              <section className="factoryiq-module anomaly-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">FACTORYIQ · ANOMALY INTELLIGENCE</span>
                    <h1>Anomalien</h1>
                    <p>
                      Echtzeit-Erkennung, Korrelation und KI-Bewertung
                      operativer Anomalien.
                    </p>
                  </div>

                  <span className="module-live-badge">
                    <i className="online-dot" />
                    Engine Connected
                  </span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi anomaly-kpi-critical">
                    <span>Kritisch</span>
                    <strong>{criticalCount}</strong>
                    <small>aktive kritische Alarme</small>
                  </div>

                  <div className="module-kpi anomaly-kpi-warning">
                    <span>Warnungen</span>
                    <strong>{warningCount}</strong>
                    <small>aktive Warnsignale</small>
                  </div>

                  <div className="module-kpi">
                    <span>Betroffene Maschinen</span>
                    <strong>{data.alarms.alarms.length > 0 ? 1 : 0}</strong>
                    <small>aktuell erkannt</small>
                  </div>

                  <div className="module-kpi">
                    <span>AI Confidence</span>
                    <strong>
                      {anomalyConfidence !== null
                        ? `${Math.round(anomalyConfidence * 100)}%`
                        : "—"}
                    </strong>
                    <small>Anomalie-Erkennung</small>
                  </div>
                </div>

                <div className="anomaly-layout">
                  <div className="anomaly-main-card">
                    <div className="anomaly-card-header">
                      <div>
                        <span className="section-eyebrow">ACTIVE ANOMALIES</span>
                        <h2>Aktuelle Anomalien</h2>
                      </div>

                      <span className="anomaly-count-badge">
                        {alarmCount} aktive Signale
                      </span>
                    </div>

                    <div className="anomaly-list">
                      {data.alarms.alarms.length > 0 ? (
                        data.alarms.alarms.map((alarm) => (
                          <div
                            className={`anomaly-row anomaly-row-${alarm.severity}`}
                            key={alarm.id}
                          >
                            <div className="anomaly-severity">
                              <span className={`anomaly-severity-dot ${alarm.severity}`} />
                              <strong>{formatLabel(alarm.severity)}</strong>
                            </div>

                            <div className="anomaly-event">
                              <strong>{alarm.message}</strong>
                              <span>
                                {alarm.id} · {alarm.machine_id}
                              </span>
                            </div>

                            <div className="anomaly-type">
                              <span>Signal</span>
                              <strong>{formatLabel(alarm.type)}</strong>
                            </div>

                            <div className="anomaly-time">
                              <span>Zeit</span>
                              <strong>
                                {new Date(alarm.timestamp).toLocaleTimeString(
                                  "de-DE",
                                  {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                  }
                                )}
                              </strong>
                            </div>
                          </div>
                        ))
                      ) : (
                        <div className="anomaly-empty">
                          <strong>Keine aktiven Anomalien</strong>
                          <span>Die Intelligence Engine meldet aktuell keine Anomalien.</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="anomaly-assessment-card">
                    <div className="anomaly-card-header">
                      <div>
                        <span className="section-eyebrow">AI ASSESSMENT</span>
                        <h2>Anomalie-Bewertung</h2>
                      </div>

                      <span className={`machine-risk-badge ${anomalySeverity.toLowerCase()}`}>
                        {formatLabel(anomalySeverity)}
                      </span>
                    </div>

                    <div className="anomaly-assessment-machine">
                      <span>Betroffene Maschine</span>
                      <strong>
                        {activeMachine?.id ?? "Keine Maschine"}
                      </strong>
                      <small>
                        {activeMachine?.name ?? "Keine aktive Maschinenzuordnung"}
                      </small>
                    </div>

                    <div className="anomaly-metrics">
                      <div>
                        <span>Vibration</span>
                        <strong>
                          {vibrationValue !== null
                            ? `${vibrationValue.toFixed(1)} ${vibrationUnit}`
                            : "—"}
                        </strong>
                        <small>
                          Grenzwert{" "}
                          {vibrationThreshold !== null
                            ? `${vibrationThreshold.toFixed(1)} ${vibrationUnit}`
                            : "—"}
                        </small>
                      </div>

                      <div>
                        <span>Confidence</span>
                        <strong>
                          {anomalyConfidence !== null
                            ? `${Math.round(anomalyConfidence * 100)}%`
                            : "—"}
                        </strong>
                        <small>AI anomaly confidence</small>
                      </div>

                      <div>
                        <span>Evidenz</span>
                        <strong>{predictionEvidence}</strong>
                        <small>unterstützende Evidence Items</small>
                      </div>

                      <div>
                        <span>Signale</span>
                        <strong>{predictionSignals.length}</strong>
                        <small>korrelierte Signale</small>
                      </div>
                    </div>

                    <div className="anomaly-signal-section">
                      <span className="section-eyebrow">CORRELATED SIGNALS</span>

                      <div className="anomaly-signal-list">
                        {predictionSignals.length > 0 ? (
                          predictionSignals.map((signal) => (
                            <span className="anomaly-signal-chip" key={signal}>
                              <i />
                              {formatLabel(signal)}
                            </span>
                          ))
                        ) : (
                          <span className="anomaly-signal-chip muted">
                            Keine korrelierten Signale
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="anomaly-intelligence-grid">
                  <div className="anomaly-prediction-card">
                    <span className="section-eyebrow">PREDICTION</span>

                    <h2>{predictionTitle}</h2>

                    <p>
                      {predictionDescription ||
                        "Keine weiterführende Prediction verfügbar."}
                    </p>

                    <div className="anomaly-evidence-row">
                      <div>
                        <span>Severity</span>
                        <strong>{formatLabel(predictionSeverity)}</strong>
                      </div>

                      <div>
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                      </div>

                      <div>
                        <span>Confidence</span>
                        <strong>
                          {primaryPrediction?.confidence
                            ? formatLabel(primaryPrediction.confidence)
                            : "—"}
                        </strong>
                      </div>
                    </div>
                  </div>

                  <div className="anomaly-cause-card">
                    <span className="section-eyebrow">ROOT CAUSE / CORRELATION</span>

                    <h2>Erkannte Zusammenhänge</h2>

                    <div className="anomaly-correlation-flow">
                      {predictionSignals.length > 0 ? (
                        predictionSignals.map((signal, index) => (
                          <div className="anomaly-correlation-item" key={signal}>
                            <span className="correlation-index">
                              {index + 1}
                            </span>
                            <strong>{formatLabel(signal)}</strong>
                          </div>
                        ))
                      ) : (
                        <div className="anomaly-correlation-item">
                          <span className="correlation-index">—</span>
                          <strong>Keine Korrelation verfügbar</strong>
                        </div>
                      )}

                      <div className="anomaly-correlation-result">
                        <span>AI Prediction</span>
                        <strong>{predictionTitle}</strong>
                      </div>
                    </div>
                  </div>

                  <div className="anomaly-decision-card">
                    <span className="section-eyebrow">AI DECISION</span>

                    <div className="anomaly-decision-flow">
                      <strong>{formatLabel(decisionType)}</strong>
                      <span>→</span>
                      <strong>{formatLabel(decisionAction)}</strong>
                    </div>

                    <p>
                      {decisionRationale ||
                        "Keine Entscheidungsbegründung verfügbar."}
                    </p>

                    <div className="anomaly-learning">
                      <span>LEARNING SIGNAL</span>
                      <strong>{formatLabel(learningAction)}</strong>
                    </div>
                  </div>
                </div>

                <div className="anomaly-history-card">
                  <div className="anomaly-card-header">
                    <div>
                      <span className="section-eyebrow">HISTORICAL SUPPORT</span>
                      <h2>Historische Evidenz</h2>
                    </div>

                    <span className="anomaly-count-badge">
                      {data.historical_patterns.entry_count} Beobachtungen
                    </span>
                  </div>

                  <div className="anomaly-history-grid">
                    <div>
                      <span>Machine History</span>
                      <strong>
                        {activeMachine?.id ?? "—"}
                      </strong>
                      <small>
                        {data.historical_patterns.entry_count} historische
                        Beobachtungen
                      </small>
                    </div>

                    <div>
                      <span>Running History</span>
                      <strong>
                        {data.historical_patterns.entry_count > 0
                          ? `${Math.round(
                              ((data.historical_patterns.status_counts.running ??
                                0) /
                                data.historical_patterns.entry_count) *
                                100
                            )}%`
                          : "—"}
                      </strong>
                      <small>
                        {data.historical_patterns.status_counts.running ?? 0}{" "}
                        Beobachtungen
                      </small>
                    </div>

                    <div>
                      <span>Warning History</span>
                      <strong>
                        {data.historical_patterns.status_counts.warning ?? 0}
                      </strong>
                      <small>historische Warnzustände</small>
                    </div>

                    <div>
                      <span>Historical Support</span>
                      <strong>
                        {primaryPrediction?.evidence?.evidence_strength
                          ? formatLabel(
                              primaryPrediction.evidence.evidence_strength
                            )
                          : "Nicht verfügbar"}
                      </strong>
                      <small>für aktuelle Prediction</small>
                    </div>
                  </div>
                </div>
              </section>
            ) : activeSection === "Predictive Maintenance" ? (
              <section className="factoryiq-module predictive-maintenance-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">PREDICTIVE MAINTENANCE</span>
                    <h1>Predictive Maintenance</h1>
                    <p>
                      Früherkennung von Maschinenrisiken auf Basis von Anomalien,
                      Predictions, Evidence und historischen Signalen.
                    </p>
                  </div>
                  <span className="module-live-badge">AI Engine Connected</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>RISK MACHINES</span>
                    <strong>
                      {anomalySeverity.toLowerCase() === "high" ? 1 : 0}
                    </strong>
                    <small>Maschinen mit erhöhtem AI-Risiko</small>
                  </div>

                  <div className="module-kpi">
                    <span>PREDICTION</span>
                    <strong>
                      {predictionScenarios.length}
                    </strong>
                    <small>aktive Prediction-Szenarien</small>
                  </div>

                  <div className="module-kpi">
                    <span>AI CONFIDENCE</span>
                    <strong>
                      {anomalyConfidence !== null
                        ? `${Math.round(anomalyConfidence * 100)}%`
                        : "—"}
                    </strong>
                    <small>Anomalie-Konfidenz</small>
                  </div>

                  <div className="module-kpi">
                    <span>MAINTENANCE</span>
                    <strong>
                      {formatLabel(data.maintenance.status)}
                    </strong>
                    <small>{data.maintenance.type}</small>
                  </div>
                </div>

                <div className="pm-grid">
                  <div className="pm-machine-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">MACHINE RISK ASSESSMENT</span>
                        <h2>{activeMachine?.id ?? "MACHINE-001"}</h2>
                      </div>

                      <span className={`machine-risk-badge ${predictionSeverity.toLowerCase()}`}>
                        {formatLabel(predictionSeverity)}
                      </span>
                    </div>

                    <div className="pm-metrics">
                      <div className="pm-metric">
                        <span>Machine</span>
                        <strong>{activeMachine?.name ?? "—"}</strong>
                        <small>
                          {activeMachine?.production_line_id ?? "Keine Linie"}
                        </small>
                      </div>

                      <div className="pm-metric">
                        <span>Vibration</span>
                        <strong>
                          {vibrationValue !== null
                            ? `${vibrationValue} ${vibrationUnit}`
                            : "—"}
                        </strong>
                        <small>
                          Threshold{" "}
                          {vibrationThreshold !== null
                            ? `${vibrationThreshold} ${vibrationUnit}`
                            : "—"}
                        </small>
                      </div>

                      <div className="pm-metric">
                        <span>Anomaly Severity</span>
                        <strong>{formatLabel(anomalySeverity)}</strong>
                        <small>
                          {predictionSignals.length} korrelierte Signale
                        </small>
                      </div>

                      <div className="pm-metric">
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                        <small>unterstützende Evidence Items</small>
                      </div>
                    </div>

                    <div className="pm-risk-panel">
                      <div className="pm-risk-heading">
                        <div>
                          <span className="section-eyebrow">CURRENT RISK SIGNAL</span>
                          <strong>{predictionTitle}</strong>
                        </div>

                        <span className="pm-risk-status">
                          {formatLabel(predictionSeverity)}
                        </span>
                      </div>

                      <p>{predictionDescription}</p>

                      <div className="signal-chip-row">
                        {predictionSignals.length > 0 ? (
                          predictionSignals.map((signal) => (
                            <span className="signal-chip" key={signal}>
                              {formatLabel(signal)}
                            </span>
                          ))
                        ) : (
                          <span className="signal-chip">
                            Keine aktiven Risikosignale
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="pm-prediction-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AI PREDICTION</span>
                        <h2>Degradation Forecast</h2>
                      </div>

                      <span className="machine-count-badge">
                        {primaryPrediction?.confidence
                          ? `Confidence ${formatLabel(primaryPrediction.confidence)}`
                          : "AI Analysis"}
                      </span>
                    </div>

                    <div className="pm-forecast">
                      <div className="pm-forecast-icon">◷</div>

                      <div>
                        <strong>{predictionTitle}</strong>
                        <p>{predictionDescription}</p>
                      </div>
                    </div>

                    <div className="pm-evidence-box">
                      <span className="section-eyebrow">EVIDENCE</span>

                      <div className="pm-evidence-grid">
                        <div>
                          <span>Evidence Count</span>
                          <strong>{predictionEvidence}</strong>
                        </div>

                        <div>
                          <span>Signals</span>
                          <strong>{predictionSignals.length}</strong>
                        </div>

                        <div>
                          <span>Machine</span>
                          <strong>
                            {activeMachine?.id ?? "—"}
                          </strong>
                        </div>

                        <div>
                          <span>Severity</span>
                          <strong>
                            {formatLabel(predictionSeverity)}
                          </strong>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pm-bottom-grid">
                  <div className="pm-action-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">MAINTENANCE STRATEGY</span>
                        <h2>AI Maintenance Decision</h2>
                      </div>

                      <span className="module-live-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="pm-decision-main">
                      <div className="pm-decision-icon">⚙</div>

                      <div>
                        <strong>{formatLabel(decisionAction)}</strong>
                        <p>{decisionRationale}</p>
                      </div>
                    </div>

                    <div className="pm-decision-grid">
                      <div>
                        <span>Learning Action</span>
                        <strong>{formatLabel(learningAction)}</strong>
                      </div>

                      <div>
                        <span>Priority</span>
                        <strong>
                          {formatLabel(
                            data.ai.learning_signal?.priority ?? "normal"
                          )}
                        </strong>
                      </div>

                      <div>
                        <span>Maintenance</span>
                        <strong>{formatLabel(data.maintenance.status)}</strong>
                      </div>

                      <div>
                        <span>Evaluation</span>
                        <strong>{evaluationScore.toFixed(2)}</strong>
                      </div>
                    </div>
                  </div>

                  <div className="pm-history-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">HISTORICAL INTELLIGENCE</span>
                        <h2>Failure & Risk History</h2>
                      </div>

                      <span className="machine-count-badge">
                        {data.historical_patterns.entry_count} observations
                      </span>
                    </div>

                    <div className="pm-history-grid">
                      <div>
                        <span>Running History</span>
                        <strong>
                          {data.historical_patterns.entry_count > 0
                            ? `${Math.round(
                                ((data.historical_patterns.status_counts.running ?? 0) /
                                  data.historical_patterns.entry_count) *
                                  100
                              )}%`
                            : "—"}
                        </strong>
                      </div>

                      <div>
                        <span>Warning History</span>
                        <strong>
                          {data.historical_patterns.status_counts.warning ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Recurring Machines</span>
                        <strong>
                          {data.historical_patterns.recurring_machine_ids.length}
                        </strong>
                      </div>

                      <div>
                        <span>Historical Support</span>
                        <strong>
                          {primaryPrediction?.evidence?.evidence_strength
                            ? formatLabel(
                                primaryPrediction.evidence.evidence_strength
                              )
                            : "Limited"}
                        </strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pm-intelligence-footer">
                  <div>
                    <span className="section-eyebrow">RECOMMENDED NEXT STEP</span>
                    <strong>
                      {decisionAction === "review_strategy"
                        ? "Maintenance-Strategie überprüfen und Maschine weiter beobachten."
                        : "AI Decision ausführen und Outcome für das Learning erfassen."}
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>

            ) : activeSection === "Qualität" ? (
              <section className="factoryiq-module quality-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">QUALITY INTELLIGENCE</span>
                    <h1>Qualität</h1>
                    <p>AI-gestützte Qualitätsbewertung aus Produktionsstatus, Anomaliesignalen und Maschinenzustand.</p>
                  </div>
                  <span className="module-live-badge">AI ENGINE CONNECTED</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>QUALITY STATUS</span>
                    <strong>{anomalySeverity.toLowerCase() === "high" ? "Risk" : "Stable"}</strong>
                    <small>abgeleitet aus aktuellen AI-Signalen</small>
                  </div>

                  <div className="module-kpi">
                    <span>OUTPUT</span>
                    <strong>{productionOutput}</strong>
                    <small>Ziel {productionTarget}</small>
                  </div>

                  <div className="module-kpi">
                    <span>OUTPUT ACHIEVEMENT</span>
                    <strong>
                      {productionTarget > 0
                        ? `${Math.round((productionOutput / productionTarget) * 100)}%`
                        : "—"}
                    </strong>
                    <small>Produktion vs. Ziel</small>
                  </div>

                  <div className="module-kpi">
                    <span>QUALITY SIGNALS</span>
                    <strong>{predictionSignals.length}</strong>
                    <small>korrelierte AI-Signale</small>
                  </div>
                </div>

                <div className="quality-grid">

                  <div className="quality-status-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AI QUALITY ASSESSMENT</span>
                        <h2>Current Quality Risk</h2>
                      </div>

                      <span className={`quality-risk-badge ${
                        anomalySeverity.toLowerCase() === "high" ? "risk" : "stable"
                      }`}>
                        {anomalySeverity.toLowerCase() === "high"
                          ? "Elevated Risk"
                          : "Stable"}
                      </span>
                    </div>

                    <div className="quality-score">
                      <div className="quality-score-ring">
                        <strong>
                          {anomalyConfidence !== null
                            ? `${Math.round(anomalyConfidence * 100)}`
                            : "—"}
                        </strong>
                        <span>AI</span>
                      </div>

                      <div className="quality-score-copy">
                        <span className="section-eyebrow">CONFIDENCE SIGNAL</span>
                        <h3>{predictionTitle}</h3>
                        <p>{predictionDescription}</p>
                      </div>
                    </div>

                    <div className="quality-signal-list">
                      <div className="quality-list-heading">
                        <span className="section-eyebrow">
                          QUALITY-RELEVANT SIGNALS
                        </span>
                        <span>{predictionSignals.length} active</span>
                      </div>

                      {predictionSignals.length > 0 ? (
                        predictionSignals.map((signal) => (
                          <div className="quality-signal-row" key={signal}>
                            <span className="quality-signal-dot" />
                            <strong>{formatLabel(signal)}</strong>
                            <span>AI detected</span>
                          </div>
                        ))
                      ) : (
                        <div className="quality-signal-empty">
                          Keine qualitätsrelevanten AI-Signale erkannt.
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="quality-production-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">
                          PRODUCTION QUALITY CONTEXT
                        </span>
                        <h2>Production vs. Target</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(data.production.status)}
                      </span>
                    </div>

                    <div className="quality-production-value">
                      <strong>{productionOutput}</strong>
                      <span>/ {productionTarget}</span>
                    </div>

                    <div className="quality-progress-track">
                      <div
                        className="quality-progress-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            productionTarget > 0
                              ? (productionOutput / productionTarget) * 100
                              : 0
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="quality-production-meta">
                      <div>
                        <span>Output</span>
                        <strong>{productionOutput}</strong>
                      </div>

                      <div>
                        <span>Target</span>
                        <strong>{productionTarget}</strong>
                      </div>

                      <div>
                        <span>Achievement</span>
                        <strong>
                          {productionTarget > 0
                            ? `${Math.round(
                                (productionOutput / productionTarget) * 100
                              )}%`
                            : "—"}
                        </strong>
                      </div>
                    </div>

                    <div className="quality-context-note">
                      <span className="section-eyebrow">ENGINE CONTEXT</span>
                      <p>
                        Die aktuelle Produktion erreicht das definierte Ziel.
                        Qualitätsrisiken werden separat aus den verfügbaren
                        Maschinen- und Anomaliesignalen bewertet.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="quality-bottom-grid">

                  <div className="quality-insight-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">ROOT CAUSE CONTEXT</span>
                        <h2>Quality Risk Drivers</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="quality-driver-grid">
                      <div>
                        <span>Machine</span>
                        <strong>{activeMachine?.id ?? "—"}</strong>
                      </div>

                      <div>
                        <span>Anomaly</span>
                        <strong>{formatLabel(anomalySeverity)}</strong>
                      </div>

                      <div>
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                      </div>

                      <div>
                        <span>AI Decision</span>
                        <strong>{formatLabel(decisionAction)}</strong>
                      </div>
                    </div>

                    <div className="quality-rationale">
                      <span className="section-eyebrow">AI RATIONALE</span>
                      <p>{decisionRationale}</p>
                    </div>
                  </div>

                  <div className="quality-history-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">
                          HISTORICAL QUALITY CONTEXT
                        </span>
                        <h2>Operational History</h2>
                      </div>

                      <span className="machine-count-badge">
                        {data.historical_patterns.entry_count} observations
                      </span>
                    </div>

                    <div className="quality-history-grid">
                      <div>
                        <span>Running</span>
                        <strong>
                          {data.historical_patterns.entry_count > 0
                            ? `${Math.round(
                                ((data.historical_patterns.status_counts.running ?? 0) /
                                  data.historical_patterns.entry_count) *
                                  100
                              )}%`
                            : "—"}
                        </strong>
                      </div>

                      <div>
                        <span>Warnings</span>
                        <strong>
                          {data.historical_patterns.status_counts.warning ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Machines</span>
                        <strong>
                          {data.historical_patterns.recurring_machine_ids.length}
                        </strong>
                      </div>

                      <div>
                        <span>Evaluation</span>
                        <strong>{evaluationScore.toFixed(2)}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="quality-footer">
                  <div>
                    <span className="section-eyebrow">
                      QUALITY INTELLIGENCE STATUS
                    </span>

                    <strong>
                      {anomalySeverity.toLowerCase() === "high"
                        ? "Erhöhtes Qualitätsrisiko erkannt – betroffene Maschine weiter beobachten und AI Decision berücksichtigen."
                        : "Kein erhöhtes Qualitätsrisiko aus den aktuell verfügbaren Engine-Signalen abgeleitet."}
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>
            ) : activeSection === "Energie" ? (
              <section className="factoryiq-module energy-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">ENERGY INTELLIGENCE</span>
                    <h1>Energie</h1>
                    <p>AI-gestützte Analyse des Energieverbrauchs im Kontext von Produktion, Maschinenzustand und Betriebsstatus.</p>
                  </div>
                  <span className="module-live-badge">AI ENGINE CONNECTED</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>ENERGY CONSUMPTION</span>
                    <strong>{data.energy.consumption}</strong>
                    <small>{data.energy.unit}</small>
                  </div>

                  <div className="module-kpi">
                    <span>ENERGY STATUS</span>
                    <strong>{formatLabel(data.energy.status)}</strong>
                    <small>aktueller Engine-Status</small>
                  </div>

                  <div className="module-kpi">
                    <span>PRODUCTION OUTPUT</span>
                    <strong>{productionOutput}</strong>
                    <small>Ziel {productionTarget}</small>
                  </div>

                  <div className="module-kpi">
                    <span>RUNNING MACHINES</span>
                    <strong>{runningMachines}/{machineCount}</strong>
                    <small>aktive Maschinen</small>
                  </div>
                </div>

                <div className="energy-main-grid">

                  <div className="energy-consumption-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">CURRENT ENERGY LOAD</span>
                        <h2>Energy Consumption</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(data.energy.status)}
                      </span>
                    </div>

                    <div className="energy-main-value">
                      <strong>{data.energy.consumption}</strong>
                      <span>{data.energy.unit}</span>
                    </div>

                    <div className="energy-load-track">
                      <div
                        className="energy-load-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            Math.max(
                              8,
                              productionTarget > 0
                                ? (productionOutput / productionTarget) * 100
                                : 8
                            )
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="energy-meta-grid">
                      <div>
                        <span>Factory</span>
                        <strong>{data.factory.name}</strong>
                      </div>

                      <div>
                        <span>Location</span>
                        <strong>{data.factory.location}</strong>
                      </div>

                      <div>
                        <span>Status</span>
                        <strong>{formatLabel(data.factory.status)}</strong>
                      </div>

                      <div>
                        <span>Machines</span>
                        <strong>{machineCount}</strong>
                      </div>
                    </div>
                  </div>

                  <div className="energy-ai-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AI ENERGY CONTEXT</span>
                        <h2>Operational Intelligence</h2>
                      </div>

                      <span className="energy-ai-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="energy-ai-signal">
                      <div className="energy-signal-icon">ϟ</div>

                      <div>
                        <span className="section-eyebrow">OPERATIONAL SIGNAL</span>
                        <h3>{formatLabel(data.ai.operational_signal)}</h3>
                        <p>
                          Die Engine bewertet den Energiezustand gemeinsam mit
                          Produktions-, Maschinen- und Anomaliesignalen.
                        </p>
                      </div>
                    </div>

                    <div className="energy-ai-grid">
                      <div>
                        <span>Prediction</span>
                        <strong>{predictionTitle}</strong>
                      </div>

                      <div>
                        <span>AI Decision</span>
                        <strong>{formatLabel(decisionAction)}</strong>
                      </div>

                      <div>
                        <span>Learning</span>
                        <strong>{formatLabel(learningAction)}</strong>
                      </div>

                      <div>
                        <span>Priority</span>
                        <strong>{formatLabel(data.ai.learning_signal.priority)}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="energy-bottom-grid">

                  <div className="energy-production-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">ENERGY / PRODUCTION CONTEXT</span>
                        <h2>Production Efficiency Context</h2>
                      </div>

                      <span className="machine-count-badge">
                        {productionTarget > 0
                          ? `${Math.round((productionOutput / productionTarget) * 100)}% target`
                          : "—"}
                      </span>
                    </div>

                    <div className="energy-production-values">
                      <div>
                        <span>Output</span>
                        <strong>{productionOutput}</strong>
                      </div>

                      <div>
                        <span>Target</span>
                        <strong>{productionTarget}</strong>
                      </div>

                      <div>
                        <span>Achievement</span>
                        <strong>
                          {productionTarget > 0
                            ? `${Math.round(
                                (productionOutput / productionTarget) * 100
                              )}%`
                            : "—"}
                        </strong>
                      </div>
                    </div>

                    <div className="energy-context-box">
                      <span className="section-eyebrow">ENGINE INTERPRETATION</span>
                      <p>
                        Der aktuelle Energieverbrauch wird zusammen mit dem
                        Produktionszustand betrachtet. Eine belastbare
                        Energieeffizienz-Kennzahl wird erst aus einer
                        konsistenten historischen Energie- und Produktionszeitreihe
                        abgeleitet.
                      </p>
                    </div>
                  </div>

                  <div className="energy-history-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">HISTORICAL CONTEXT</span>
                        <h2>Operational Pattern</h2>
                      </div>

                      <span className="machine-count-badge">
                        {data.historical_patterns.entry_count} observations
                      </span>
                    </div>

                    <div className="energy-history-grid">
                      <div>
                        <span>Running</span>
                        <strong>
                          {data.historical_patterns.status_counts.running ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Warnings</span>
                        <strong>
                          {data.historical_patterns.status_counts.warning ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Machines</span>
                        <strong>
                          {data.historical_patterns.recurring_machine_ids.length}
                        </strong>
                      </div>

                      <div>
                        <span>Evaluation</span>
                        <strong>{evaluationScore.toFixed(2)}</strong>
                      </div>
                    </div>

                    <div className="energy-history-note">
                      <span className="section-eyebrow">AI OBSERVATION</span>
                      <p>
                        Die historische Betriebsstruktur wird vom Engine-Kontext
                        für weitere Entscheidungen und Lernsignale berücksichtigt.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="energy-footer">
                  <div>
                    <span className="section-eyebrow">ENERGY INTELLIGENCE STATUS</span>
                    <strong>
                      Energieverbrauch: {data.energy.consumption} {data.energy.unit}
                      {" · "}
                      Status: {formatLabel(data.energy.status)}
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>
            ) : activeSection === "OEE & Performance" ? (
              <section className="factoryiq-module oee-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">OEE & PERFORMANCE INTELLIGENCE</span>
                    <h1>OEE & Performance</h1>
                    <p>Produktionsleistung, Maschinenverfügbarkeit und AI-Signale in einem operativen Performance-Kontext.</p>
                  </div>
                  <span className="module-live-badge">AI ENGINE CONNECTED</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>PRODUCTION OUTPUT</span>
                    <strong>{productionOutput}</strong>
                    <small>aktuelle Produktion</small>
                  </div>

                  <div className="module-kpi">
                    <span>TARGET ACHIEVEMENT</span>
                    <strong>
                      {productionTarget > 0
                        ? `${Math.round((productionOutput / productionTarget) * 100)}%`
                        : "—"}
                    </strong>
                    <small>Output vs. Ziel</small>
                  </div>

                  <div className="module-kpi">
                    <span>AVAILABILITY CONTEXT</span>
                    <strong>
                      {machineCount > 0
                        ? `${Math.round((runningMachines / machineCount) * 100)}%`
                        : "—"}
                    </strong>
                    <small>laufende Maschinen</small>
                  </div>

                  <div className="module-kpi">
                    <span>HISTORICAL OBSERVATIONS</span>
                    <strong>{data.historical_patterns.entry_count}</strong>
                    <small>Engine-Beobachtungen</small>
                  </div>
                </div>

                <div className="oee-status-banner">
                  <div>
                    <span className="section-eyebrow">OEE DATA STATUS</span>
                    <strong>Operational performance data available</strong>
                    <p>
                      Die Engine stellt Produktions-, Maschinen- und historische
                      Betriebsdaten bereit. Eine vollständige OEE-Kennzahl wird
                      erst berechnet, sobald Availability, Performance und Quality
                      als belastbare Zeitreihen vorliegen.
                    </p>
                  </div>

                  <span className="oee-data-badge">PARTIAL OEE DATA</span>
                </div>

                <div className="oee-main-grid">

                  <div className="oee-performance-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">PERFORMANCE OVERVIEW</span>
                        <h2>Production Performance</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(data.production.status)}
                      </span>
                    </div>

                    <div className="oee-production-value">
                      <strong>{productionOutput}</strong>
                      <span>units</span>
                    </div>

                    <div className="oee-target-row">
                      <div>
                        <span>Production Target</span>
                        <strong>{productionTarget}</strong>
                      </div>

                      <div>
                        <span>Achievement</span>
                        <strong>
                          {productionTarget > 0
                            ? `${Math.round(
                                (productionOutput / productionTarget) * 100
                              )}%`
                            : "—"}
                        </strong>
                      </div>
                    </div>

                    <div className="oee-progress-track">
                      <div
                        className="oee-progress-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            productionTarget > 0
                              ? (productionOutput / productionTarget) * 100
                              : 0
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="oee-performance-note">
                      <span className="section-eyebrow">ENGINE INTERPRETATION</span>
                      <p>
                        Der aktuelle Output wird direkt gegen das Produktionsziel
                        gestellt. Diese Kennzahl beschreibt die Zielerreichung,
                        nicht den vollständigen OEE.
                      </p>
                    </div>
                  </div>

                  <div className="oee-availability-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AVAILABILITY CONTEXT</span>
                        <h2>Machine Availability</h2>
                      </div>

                      <span className="oee-status-badge">
                        {runningMachines === machineCount
                          ? "ALL RUNNING"
                          : "PARTIAL"}
                      </span>
                    </div>

                    <div className="oee-availability-value">
                      <strong>
                        {machineCount > 0
                          ? `${Math.round(
                              (runningMachines / machineCount) * 100
                            )}`
                          : "—"}
                      </strong>
                      <span>%</span>
                    </div>

                    <div className="oee-availability-track">
                      <div
                        className="oee-availability-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            machineCount > 0
                              ? (runningMachines / machineCount) * 100
                              : 0
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="oee-machine-stats">
                      <div>
                        <span>Running</span>
                        <strong>{runningMachines}</strong>
                      </div>

                      <div>
                        <span>Total</span>
                        <strong>{machineCount}</strong>
                      </div>

                      <div>
                        <span>Warnings</span>
                        <strong>{warningCount}</strong>
                      </div>

                      <div>
                        <span>Critical</span>
                        <strong>{criticalCount}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="oee-bottom-grid">

                  <div className="oee-components-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">OEE COMPONENTS</span>
                        <h2>Measurement Coverage</h2>
                      </div>

                      <span className="machine-count-badge">ENGINE STATUS</span>
                    </div>

                    <div className="oee-component-list">

                      <div className="oee-component-row">
                        <div className="oee-component-index">01</div>
                        <div>
                          <strong>Availability</strong>
                          <span>Maschinenstatus und laufende Anlagen vorhanden</span>
                        </div>
                        <b className="oee-component-ready">AVAILABLE</b>
                      </div>

                      <div className="oee-component-row">
                        <div className="oee-component-index">02</div>
                        <div>
                          <strong>Performance</strong>
                          <span>Produktion und Zielwert vorhanden</span>
                        </div>
                        <b className="oee-component-ready">AVAILABLE</b>
                      </div>

                      <div className="oee-component-row">
                        <div className="oee-component-index">03</div>
                        <div>
                          <strong>Quality</strong>
                          <span>Keine belastbare Ausschuss-/Gutteil-Zeitreihe vorhanden</span>
                        </div>
                        <b className="oee-component-pending">PENDING</b>
                      </div>
                    </div>

                    <div className="oee-component-note">
                      <span className="section-eyebrow">NEXT DATA REQUIREMENT</span>
                      <p>
                        Für einen produktiven OEE-Wert müssen Gutteile,
                        Ausschuss, Zykluszeit und geplante bzw. ungeplante
                        Stillstandszeiten historisch erfasst werden.
                      </p>
                    </div>
                  </div>

                  <div className="oee-ai-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AI PERFORMANCE INTELLIGENCE</span>
                        <h2>Current AI Signal</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="oee-ai-highlight">
                      <span className="section-eyebrow">OPERATIONAL SIGNAL</span>
                      <h3>{formatLabel(data.ai.operational_signal)}</h3>
                      <p>{predictionDescription}</p>
                    </div>

                    <div className="oee-ai-grid">
                      <div>
                        <span>Prediction</span>
                        <strong>{predictionTitle}</strong>
                      </div>

                      <div>
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                      </div>

                      <div>
                        <span>Decision</span>
                        <strong>{formatLabel(decisionAction)}</strong>
                      </div>

                      <div>
                        <span>Learning</span>
                        <strong>{formatLabel(learningAction)}</strong>
                      </div>
                    </div>

                    <div className="oee-ai-rationale">
                      <span className="section-eyebrow">AI RATIONALE</span>
                      <p>{decisionRationale}</p>
                    </div>
                  </div>
                </div>

                <div className="oee-footer">
                  <div>
                    <span className="section-eyebrow">PERFORMANCE INTELLIGENCE STATUS</span>
                    <strong>
                      Output {productionOutput}/{productionTarget}
                      {" · "}
                      {runningMachines}/{machineCount} Maschinen aktiv
                      {" · "}
                      {data.historical_patterns.entry_count} historische Beobachtungen
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>
            ) : activeSection === "Aufträge" ? (
              <section className="factoryiq-module orders-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">ORDER INTELLIGENCE</span>
                    <h1>Aufträge</h1>
                    <p>Produktionsaufträge im Kontext von Output, Zielerreichung, Maschinenstatus und AI-Entscheidungen.</p>
                  </div>
                  <span className="module-live-badge">AI ENGINE CONNECTED</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>PRODUCTION OUTPUT</span>
                    <strong>{productionOutput}</strong>
                    <small>aktueller Output</small>
                  </div>

                  <div className="module-kpi">
                    <span>PRODUCTION TARGET</span>
                    <strong>{productionTarget}</strong>
                    <small>aktuelles Produktionsziel</small>
                  </div>

                  <div className="module-kpi">
                    <span>TARGET ACHIEVEMENT</span>
                    <strong>
                      {productionTarget > 0
                        ? `${Math.round((productionOutput / productionTarget) * 100)}%`
                        : "—"}
                    </strong>
                    <small>Output vs. Ziel</small>
                  </div>

                  <div className="module-kpi">
                    <span>ACTIVE MACHINES</span>
                    <strong>{runningMachines}/{machineCount}</strong>
                    <small>laufende Maschinen</small>
                  </div>
                </div>

                <div className="orders-status-banner">
                  <div>
                    <span className="section-eyebrow">ORDER DATA STATUS</span>
                    <strong>Production execution data available</strong>
                    <p>
                      Die Engine liefert aktuell Produktionsoutput, Zielwerte,
                      Maschinenstatus und AI-Signale. Eine vollständige
                      Auftragsverwaltung benötigt zusätzlich persistierte
                      Auftrags-, Mengen-, Termin- und Statusdaten.
                    </p>
                  </div>

                  <span className="orders-data-badge">EXECUTION CONTEXT</span>
                </div>

                <div className="orders-main-grid">

                  <div className="orders-progress-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">ORDER EXECUTION</span>
                        <h2>Production Target</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(data.production.status)}
                      </span>
                    </div>

                    <div className="orders-progress-value">
                      <strong>
                        {productionTarget > 0
                          ? `${Math.round(
                              (productionOutput / productionTarget) * 100
                            )}`
                          : "—"}
                      </strong>
                      <span>% complete</span>
                    </div>

                    <div className="orders-progress-track">
                      <div
                        className="orders-progress-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            productionTarget > 0
                              ? (productionOutput / productionTarget) * 100
                              : 0
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="orders-target-grid">
                      <div>
                        <span>Output</span>
                        <strong>{productionOutput}</strong>
                      </div>

                      <div>
                        <span>Target</span>
                        <strong>{productionTarget}</strong>
                      </div>

                      <div>
                        <span>Remaining</span>
                        <strong>
                          {Math.max(
                            0,
                            productionTarget - productionOutput
                          )}
                        </strong>
                      </div>
                    </div>

                    <div className="orders-context-note">
                      <span className="section-eyebrow">EXECUTION CONTEXT</span>
                      <p>
                        Die aktuelle Produktion wird gegen das definierte Ziel
                        bewertet. Dies bildet den operativen Ausführungsstatus
                        ab, ersetzt aber keine vollständige Auftragsverwaltung.
                      </p>
                    </div>
                  </div>

                  <div className="orders-machine-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">CAPACITY CONTEXT</span>
                        <h2>Machine Execution</h2>
                      </div>

                      <span className="orders-status-badge">
                        {runningMachines === machineCount
                          ? "RUNNING"
                          : "PARTIAL"}
                      </span>
                    </div>

                    <div className="orders-machine-value">
                      <strong>{runningMachines}</strong>
                      <span>/ {machineCount} machines running</span>
                    </div>

                    <div className="orders-machine-track">
                      <div
                        className="orders-machine-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            machineCount > 0
                              ? (runningMachines / machineCount) * 100
                              : 0
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="orders-machine-grid">
                      <div>
                        <span>Running</span>
                        <strong>{runningMachines}</strong>
                      </div>

                      <div>
                        <span>Total</span>
                        <strong>{machineCount}</strong>
                      </div>

                      <div>
                        <span>Warnings</span>
                        <strong>{warningCount}</strong>
                      </div>

                      <div>
                        <span>Critical</span>
                        <strong>{criticalCount}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="orders-bottom-grid">

                  <div className="orders-ai-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AI ORDER CONTEXT</span>
                        <h2>Execution Intelligence</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="orders-ai-highlight">
                      <span className="section-eyebrow">OPERATIONAL SIGNAL</span>
                      <h3>{formatLabel(data.ai.operational_signal)}</h3>
                      <p>{predictionDescription}</p>
                    </div>

                    <div className="orders-ai-grid">
                      <div>
                        <span>Prediction</span>
                        <strong>{predictionTitle}</strong>
                      </div>

                      <div>
                        <span>Decision</span>
                        <strong>{formatLabel(decisionAction)}</strong>
                      </div>

                      <div>
                        <span>Learning</span>
                        <strong>{formatLabel(learningAction)}</strong>
                      </div>

                      <div>
                        <span>Priority</span>
                        <strong>
                          {formatLabel(data.ai.learning_signal.priority)}
                        </strong>
                      </div>
                    </div>

                    <div className="orders-rationale">
                      <span className="section-eyebrow">AI RATIONALE</span>
                      <p>{decisionRationale}</p>
                    </div>
                  </div>

                  <div className="orders-history-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">ORDER EXECUTION HISTORY</span>
                        <h2>Operational Pattern</h2>
                      </div>

                      <span className="machine-count-badge">
                        {data.historical_patterns.entry_count} observations
                      </span>
                    </div>

                    <div className="orders-history-grid">
                      <div>
                        <span>Running</span>
                        <strong>
                          {data.historical_patterns.status_counts.running ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Warnings</span>
                        <strong>
                          {data.historical_patterns.status_counts.warning ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Machines</span>
                        <strong>
                          {data.historical_patterns.recurring_machine_ids.length}
                        </strong>
                      </div>

                      <div>
                        <span>Evaluation</span>
                        <strong>{evaluationScore.toFixed(2)}</strong>
                      </div>
                    </div>

                    <div className="orders-history-note">
                      <span className="section-eyebrow">ENGINE OBSERVATION</span>
                      <p>
                        Historische Betriebsdaten werden für die Bewertung
                        zukünftiger Produktionsentscheidungen und Lernsignale
                        herangezogen.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="orders-footer">
                  <div>
                    <span className="section-eyebrow">ORDER INTELLIGENCE STATUS</span>
                    <strong>
                      Produktionsziel {productionOutput}/{productionTarget}
                      {" · "}
                      {runningMachines}/{machineCount} Maschinen aktiv
                      {" · "}
                      AI Decision: {formatLabel(decisionAction)}
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>
            ) : activeSection === "Material & Lager" ? (
              <section className="factoryiq-module material-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">MATERIAL & INVENTORY INTELLIGENCE</span>
                    <h1>Material & Lager</h1>
                    <p>Material- und Lagerkontext für Produktionssicherheit, Anlagenbetrieb und zukünftige AI-gestützte Bestandsplanung.</p>
                  </div>
                  <span className="module-live-badge">AI ENGINE CONNECTED</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>INVENTORY DATA</span>
                    <strong>Pending</strong>
                    <small>Bestandsdaten noch nicht angebunden</small>
                  </div>

                  <div className="module-kpi">
                    <span>MATERIAL SIGNALS</span>
                    <strong>0</strong>
                    <small>aktuell verfügbare Materialszenarien</small>
                  </div>

                  <div className="module-kpi">
                    <span>PRODUCTION OUTPUT</span>
                    <strong>{productionOutput}</strong>
                    <small>Ziel {productionTarget}</small>
                  </div>

                  <div className="module-kpi">
                    <span>ACTIVE MACHINES</span>
                    <strong>{runningMachines}/{machineCount}</strong>
                    <small>Produktionskapazität im aktuellen Zustand</small>
                  </div>
                </div>

                <div className="material-status-banner">
                  <div>
                    <span className="section-eyebrow">INVENTORY DATA STATUS</span>
                    <strong>Material and stock integration pending</strong>
                    <p>
                      Die aktuelle FactoryIQ Engine verfügt über Produktions-,
                      Maschinen-, Alarm- und AI-Daten. Eine echte Lageranalyse
                      benötigt zusätzlich Materialstämme, Bestände,
                      Lagerorte, Mindestbestände und Materialbewegungen.
                    </p>
                  </div>

                  <span className="material-data-badge">DATA SOURCE REQUIRED</span>
                </div>

                <div className="material-main-grid">

                  <div className="material-production-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">MATERIAL / PRODUCTION CONTEXT</span>
                        <h2>Production Dependency</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(data.production.status)}
                      </span>
                    </div>

                    <div className="material-production-value">
                      <strong>{productionOutput}</strong>
                      <span>/ {productionTarget} output</span>
                    </div>

                    <div className="material-progress-track">
                      <div
                        className="material-progress-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            productionTarget > 0
                              ? (productionOutput / productionTarget) * 100
                              : 0
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="material-production-grid">
                      <div>
                        <span>Output</span>
                        <strong>{productionOutput}</strong>
                      </div>

                      <div>
                        <span>Target</span>
                        <strong>{productionTarget}</strong>
                      </div>

                      <div>
                        <span>Achievement</span>
                        <strong>
                          {productionTarget > 0
                            ? `${Math.round(
                                (productionOutput / productionTarget) * 100
                              )}%`
                            : "—"}
                        </strong>
                      </div>
                    </div>

                    <div className="material-context-note">
                      <span className="section-eyebrow">OPERATIONAL CONTEXT</span>
                      <p>
                        Produktionsleistung ist vorhanden, aber die Engine kann
                        derzeit nicht feststellen, welche Materialien für den
                        aktuellen Output verbraucht wurden oder wann ein Bestand
                        kritisch wird.
                      </p>
                    </div>
                  </div>

                  <div className="material-machine-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">SUPPLY DEPENDENCY</span>
                        <h2>Production Capacity</h2>
                      </div>

                      <span className="material-status-badge">
                        {runningMachines === machineCount
                          ? "RUNNING"
                          : "PARTIAL"}
                      </span>
                    </div>

                    <div className="material-machine-value">
                      <strong>{runningMachines}</strong>
                      <span>/ {machineCount} machines running</span>
                    </div>

                    <div className="material-machine-track">
                      <div
                        className="material-machine-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            machineCount > 0
                              ? (runningMachines / machineCount) * 100
                              : 0
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="material-machine-grid">
                      <div>
                        <span>Running</span>
                        <strong>{runningMachines}</strong>
                      </div>

                      <div>
                        <span>Total</span>
                        <strong>{machineCount}</strong>
                      </div>

                      <div>
                        <span>Warnings</span>
                        <strong>{warningCount}</strong>
                      </div>

                      <div>
                        <span>Critical</span>
                        <strong>{criticalCount}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="material-bottom-grid">

                  <div className="material-data-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">INVENTORY COVERAGE</span>
                        <h2>Required Data Model</h2>
                      </div>

                      <span className="machine-count-badge">PLANNED</span>
                    </div>

                    <div className="material-data-list">

                      <div className="material-data-row">
                        <div className="material-data-index">01</div>
                        <div>
                          <strong>Material Master</strong>
                          <span>Materialnummer, Bezeichnung, Einheit und Kategorie</span>
                        </div>
                        <b className="material-pending">PENDING</b>
                      </div>

                      <div className="material-data-row">
                        <div className="material-data-index">02</div>
                        <div>
                          <strong>Stock Levels</strong>
                          <span>Bestand, verfügbarer Bestand und reservierte Mengen</span>
                        </div>
                        <b className="material-pending">PENDING</b>
                      </div>

                      <div className="material-data-row">
                        <div className="material-data-index">03</div>
                        <div>
                          <strong>Warehouse Locations</strong>
                          <span>Lagerorte, Zonen und Materialbewegungen</span>
                        </div>
                        <b className="material-pending">PENDING</b>
                      </div>

                      <div className="material-data-row">
                        <div className="material-data-index">04</div>
                        <div>
                          <strong>Consumption History</strong>
                          <span>Materialverbrauch je Auftrag und Produktionszeitraum</span>
                        </div>
                        <b className="material-pending">PENDING</b>
                      </div>
                    </div>

                    <div className="material-data-note">
                      <span className="section-eyebrow">NEXT INTEGRATION</span>
                      <p>
                        Nach Anbindung dieser Daten kann FactoryIQ
                        Bestandsrisiken, Materialengpässe und den Einfluss auf
                        Produktionsaufträge AI-gestützt bewerten.
                      </p>
                    </div>
                  </div>

                  <div className="material-ai-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AI MATERIAL CONTEXT</span>
                        <h2>Production Risk Intelligence</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="material-ai-highlight">
                      <span className="section-eyebrow">CURRENT SIGNAL</span>
                      <h3>{formatLabel(data.ai.operational_signal)}</h3>
                      <p>{predictionDescription}</p>
                    </div>

                    <div className="material-ai-grid">
                      <div>
                        <span>Prediction</span>
                        <strong>{predictionTitle}</strong>
                      </div>

                      <div>
                        <span>Decision</span>
                        <strong>{formatLabel(decisionAction)}</strong>
                      </div>

                      <div>
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                      </div>

                      <div>
                        <span>Learning</span>
                        <strong>{formatLabel(learningAction)}</strong>
                      </div>
                    </div>

                    <div className="material-rationale">
                      <span className="section-eyebrow">AI RATIONALE</span>
                      <p>{decisionRationale}</p>
                    </div>
                  </div>
                </div>

                <div className="material-footer">
                  <div>
                    <span className="section-eyebrow">MATERIAL & INVENTORY STATUS</span>
                    <strong>
                      Bestandsdaten noch nicht angebunden
                      {" · "}
                      Produktionsoutput {productionOutput}/{productionTarget}
                      {" · "}
                      {runningMachines}/{machineCount} Maschinen aktiv
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>
            ) : activeSection === "Reports" ? (
              <section className="factoryiq-module reports-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">ENTERPRISE REPORTING</span>
                    <h1>Reports</h1>
                    <p>Operative Produktions-, Maschinen- und AI-Kennzahlen für Management und Engineering.</p>
                  </div>
                  <span className="module-live-badge">LIVE ENGINE DATA</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>PRODUCTION</span>
                    <strong>{productionOutput}/{productionTarget}</strong>
                    <small>Output vs. Ziel</small>
                  </div>

                  <div className="module-kpi">
                    <span>MACHINES</span>
                    <strong>{runningMachines}/{machineCount}</strong>
                    <small>laufende Maschinen</small>
                  </div>

                  <div className="module-kpi">
                    <span>ALARMS</span>
                    <strong>{alarmCount}</strong>
                    <small>{criticalCount} kritisch · {warningCount} Warnungen</small>
                  </div>

                  <div className="module-kpi">
                    <span>ENERGY</span>
                    <strong>{data.energy.consumption}</strong>
                    <small>{data.energy.unit}</small>
                  </div>
                </div>

                <div className="reports-status-banner">
                  <div>
                    <span className="section-eyebrow">REPORTING STATUS</span>
                    <strong>FactoryIQ operational intelligence available</strong>
                    <p>
                      Der aktuelle Engine-Zustand kann für operative Reports,
                      Management-Übersichten und Engineering-Analysen
                      zusammengeführt werden.
                    </p>
                  </div>

                  <span className="reports-status-badge">LIVE DATA</span>
                </div>

                <div className="reports-main-grid">

                  <div className="report-card report-overview-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">EXECUTIVE OVERVIEW</span>
                        <h2>Operational Summary</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(data.factory.status)}
                      </span>
                    </div>

                    <div className="report-summary-grid">
                      <div>
                        <span>Factory</span>
                        <strong>{data.factory.name}</strong>
                      </div>

                      <div>
                        <span>Location</span>
                        <strong>{data.factory.location}</strong>
                      </div>

                      <div>
                        <span>Production</span>
                        <strong>
                          {productionTarget > 0
                            ? `${Math.round(
                                (productionOutput / productionTarget) * 100
                              )}%`
                            : "—"}
                        </strong>
                      </div>

                      <div>
                        <span>Energy</span>
                        <strong>
                          {data.energy.consumption} {data.energy.unit}
                        </strong>
                      </div>

                      <div>
                        <span>Alarms</span>
                        <strong>{alarmCount}</strong>
                      </div>

                      <div>
                        <span>AI Signal</span>
                        <strong>{formatLabel(data.ai.operational_signal)}</strong>
                      </div>
                    </div>

                    <div className="report-highlight">
                      <span className="section-eyebrow">EXECUTIVE INTERPRETATION</span>
                      <p>
                        Produktion, Maschinenzustand, Energie und AI-Signale
                        werden in einem gemeinsamen operativen Kontext
                        dargestellt. Kritische Alarme und erkannte
                        Anomaliesignale bleiben für die weitere Analyse sichtbar.
                      </p>
                    </div>
                  </div>

                  <div className="report-card report-ai-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">AI REPORTING</span>
                        <h2>Intelligence Summary</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="report-ai-highlight">
                      <span className="section-eyebrow">PRIMARY PREDICTION</span>
                      <h3>{predictionTitle}</h3>
                      <p>{predictionDescription}</p>
                    </div>

                    <div className="report-ai-grid">
                      <div>
                        <span>Decision</span>
                        <strong>{formatLabel(decisionAction)}</strong>
                      </div>

                      <div>
                        <span>Learning</span>
                        <strong>{formatLabel(learningAction)}</strong>
                      </div>

                      <div>
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                      </div>

                      <div>
                        <span>Evaluation</span>
                        <strong>{evaluationScore.toFixed(2)}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="reports-bottom-grid">

                  <div className="report-card report-alarm-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">INCIDENT REPORT</span>
                        <h2>Alarm Overview</h2>
                      </div>

                      <span className="reports-critical-badge">
                        {criticalCount} critical
                      </span>
                    </div>

                    <div className="report-alarm-grid">
                      <div>
                        <span>Total</span>
                        <strong>{alarmCount}</strong>
                      </div>

                      <div>
                        <span>Critical</span>
                        <strong>{criticalCount}</strong>
                      </div>

                      <div>
                        <span>Warning</span>
                        <strong>{warningCount}</strong>
                      </div>

                      <div>
                        <span>Severity</span>
                        <strong>{formatLabel(anomalySeverity)}</strong>
                      </div>
                    </div>

                    <div className="report-alarm-note">
                      <span className="section-eyebrow">CURRENT AI CONTEXT</span>
                      <p>
                        {predictionSignals.length > 0
                          ? `${predictionSignals.length} relevante AI-Signale sind aktuell mit dem operativen Zustand verknüpft.`
                          : "Aktuell sind keine zusätzlichen AI-Signale verfügbar."}
                      </p>
                    </div>
                  </div>

                  <div className="report-card report-history-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">HISTORICAL REPORTING</span>
                        <h2>Operational History</h2>
                      </div>

                      <span className="machine-count-badge">
                        {data.historical_patterns.entry_count} observations
                      </span>
                    </div>

                    <div className="report-history-grid">
                      <div>
                        <span>Running</span>
                        <strong>
                          {data.historical_patterns.status_counts.running ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Warnings</span>
                        <strong>
                          {data.historical_patterns.status_counts.warning ?? 0}
                        </strong>
                      </div>

                      <div>
                        <span>Machines</span>
                        <strong>
                          {data.historical_patterns.recurring_machine_ids.length}
                        </strong>
                      </div>

                      <div>
                        <span>Evaluation</span>
                        <strong>{evaluationScore.toFixed(2)}</strong>
                      </div>
                    </div>

                    <div className="report-history-note">
                      <span className="section-eyebrow">REPORTING CONTEXT</span>
                      <p>
                        Historische Betriebsbeobachtungen bilden die Grundlage
                        für Trendanalysen, wiederkehrende Muster und zukünftige
                        AI-Lernsignale.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="report-footer">
                  <div>
                    <span className="section-eyebrow">REPORT DATA COVERAGE</span>
                    <strong>
                      FactoryIQ Engine · {data.historical_patterns.entry_count} historische Beobachtungen
                      {" · "}
                      {predictionScenarios.length} AI-Szenarien
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>
            ) : activeSection === "KI Insights" ? (
              <section className="factoryiq-module ai-insights-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">FACTORYIQ INTELLIGENCE</span>
                    <h1>KI Insights</h1>
                    <p>Prediction, Root Cause, Decision, Evidence und Learning aus der AIHelixia Intelligence Engine.</p>
                  </div>
                  <span className="module-live-badge">AI ENGINE CONNECTED</span>
                </div>

                <div className="module-kpis">
                  <div className="module-kpi">
                    <span>AI SIGNAL</span>
                    <strong>{formatLabel(data.ai.operational_signal)}</strong>
                    <small>aktueller operativer Zustand</small>
                  </div>

                  <div className="module-kpi">
                    <span>PREDICTIONS</span>
                    <strong>{predictionScenarios.length}</strong>
                    <small>erkannte AI-Szenarien</small>
                  </div>

                  <div className="module-kpi">
                    <span>DECISION</span>
                    <strong>{formatLabel(decisionType)}</strong>
                    <small>aktuelle Engine-Entscheidung</small>
                  </div>

                  <div className="module-kpi">
                    <span>EVALUATION</span>
                    <strong>{evaluationScore.toFixed(2)}</strong>
                    <small>aktueller Evaluation Score</small>
                  </div>
                </div>

                <div className="ai-insights-hero">
                  <div className="ai-insights-hero-copy">
                    <span className="section-eyebrow">PRIMARY INTELLIGENCE SIGNAL</span>
                    <h2>{predictionTitle}</h2>
                    <p>{predictionDescription}</p>

                    <div className="ai-insights-signal-row">
                      {predictionSignals.length > 0 ? (
                        predictionSignals.map((signal) => (
                          <span className="ai-insight-signal" key={signal}>
                            {formatLabel(signal)}
                          </span>
                        ))
                      ) : (
                        <span className="ai-insight-signal muted">
                          No active signal
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="ai-insights-confidence">
                    <span className="section-eyebrow">AI CONFIDENCE</span>
                    <strong>
                      {anomalyConfidence !== null
                        ? `${Math.round(anomalyConfidence * 100)}%`
                        : "—"}
                    </strong>
                    <span>{formatLabel(anomalySeverity)} severity</span>
                  </div>
                </div>

                <div className="ai-insights-main-grid">

                  <div className="ai-insight-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">01 · PREDICTION</span>
                        <h2>AI Prediction</h2>
                      </div>

                      <span className="ai-version-badge">
                        {data.ai.prediction.version}
                      </span>
                    </div>

                    <div className="ai-insight-primary">
                      <span className="section-eyebrow">PRIMARY SCENARIO</span>
                      <h3>{predictionTitle}</h3>
                      <p>{predictionDescription}</p>
                    </div>

                    <div className="ai-detail-grid">
                      <div>
                        <span>Scenarios</span>
                        <strong>{predictionScenarios.length}</strong>
                      </div>

                      <div>
                        <span>Evidence</span>
                        <strong>{predictionEvidence}</strong>
                      </div>

                      <div>
                        <span>Severity</span>
                        <strong>{formatLabel(predictionSeverity)}</strong>
                      </div>

                      <div>
                        <span>Confidence</span>
                        <strong>
                          {primaryPrediction?.confidence
                            ? formatLabel(primaryPrediction.confidence)
                            : "—"}
                        </strong>
                      </div>
                    </div>
                  </div>

                  <div className="ai-insight-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">02 · ROOT CAUSE</span>
                        <h2>Root Cause Analysis</h2>
                      </div>

                      <span className="machine-count-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="ai-rootcause-highlight">
                      <span className="section-eyebrow">PRIMARY HYPOTHESIS</span>
                      <h3>
                        {data.ai.decision.root_cause?.primary_type
                          ? formatLabel(data.ai.decision.root_cause.primary_type)
                          : "Insufficient signal"}
                      </h3>
                      <p>
                        {data.ai.decision.root_cause?.hypothesis_count ?? 0} Root-Cause-Hypothesen
                        {" · "}
                        Confidence: {formatLabel(
                          data.ai.decision.root_cause?.confidence ?? "—"
                        )}
                      </p>
                    </div>

                    <div className="ai-detail-grid">
                      <div>
                        <span>Evidence</span>
                        <strong>
                          {data.ai.decision.evidence?.evidence_count ?? predictionEvidence}
                        </strong>
                      </div>

                      <div>
                        <span>Strength</span>
                        <strong>
                          {formatLabel(
                            data.ai.decision.evidence?.evidence_strength ?? "—"
                          )}
                        </strong>
                      </div>

                      <div>
                        <span>Machine</span>
                        <strong>{activeMachine?.id ?? "—"}</strong>
                      </div>

                      <div>
                        <span>Signals</span>
                        <strong>{predictionSignals.length}</strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="ai-insights-bottom-grid">

                  <div className="ai-insight-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">03 · DECISION</span>
                        <h2>AI Decision</h2>
                      </div>

                      <span className="ai-decision-badge">
                        {formatLabel(decisionType)}
                      </span>
                    </div>

                    <div className="ai-decision-action">
                      <span className="section-eyebrow">RECOMMENDED ACTION</span>
                      <strong>{formatLabel(decisionAction)}</strong>
                    </div>

                    <div className="ai-decision-rationale">
                      <span className="section-eyebrow">RATIONALE</span>
                      <p>{decisionRationale}</p>
                    </div>

                    <div className="ai-detail-grid">
                      <div>
                        <span>Priority</span>
                        <strong>
                          {formatLabel(data.ai.learning_signal.priority)}
                        </strong>
                      </div>

                      <div>
                        <span>Action Status</span>
                        <strong>
                          {formatLabel(data.ai.evaluation.action_status)}
                        </strong>
                      </div>

                      <div>
                        <span>Execution</span>
                        <strong>
                          {formatLabel(data.ai.evaluation.execution_evaluation ?? "—")}
                        </strong>
                      </div>

                      <div>
                        <span>Outcome</span>
                        <strong>
                          {formatLabel(data.ai.evaluation.outcome_status ?? "—")}
                        </strong>
                      </div>
                    </div>
                  </div>

                  <div className="ai-insight-card">
                    <div className="machine-card-heading">
                      <div>
                        <span className="section-eyebrow">04 · LEARNING</span>
                        <h2>Learning Signal</h2>
                      </div>

                      <span className="ai-learning-badge">
                        {formatLabel(learningAction)}
                      </span>
                    </div>

                    <div className="ai-learning-highlight">
                      <span className="section-eyebrow">CURRENT LEARNING ACTION</span>
                      <h3>{formatLabel(learningAction)}</h3>
                      <p>{learningReason}</p>
                    </div>

                    <div className="ai-detail-grid">
                      <div>
                        <span>Priority</span>
                        <strong>
                          {formatLabel(data.ai.learning_signal.priority)}
                        </strong>
                      </div>

                      <div>
                        <span>Evaluation</span>
                        <strong>{evaluationScore.toFixed(2)}</strong>
                      </div>

                      <div>
                        <span>Historical Entries</span>
                        <strong>
                          {data.historical_patterns.entry_count}
                        </strong>
                      </div>

                      <div>
                        <span>Historical Machines</span>
                        <strong>
                          {data.historical_patterns.recurring_machine_ids.length}
                        </strong>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="ai-insights-evidence-card">
                  <div className="machine-card-heading">
                    <div>
                      <span className="section-eyebrow">05 · EVIDENCE</span>
                      <h2>Evidence & Historical Support</h2>
                    </div>

                    <span className="machine-count-badge">
                      {predictionEvidence} evidence
                    </span>
                  </div>

                  <div className="ai-evidence-grid">
                    <div>
                      <span>Supporting Signals</span>
                      <strong>
                        {predictionSignals.length > 0
                          ? predictionSignals.map(formatLabel).join(" · ")
                          : "None"}
                      </strong>
                    </div>

                    <div>
                      <span>Correlated Machines</span>
                      <strong>
                        {data.ai.prediction.evidence_summary?.historical_supported_scenarios !== undefined
                          ? data.historical_patterns.recurring_machine_ids.join(" · ") || "None"
                          : "—"}
                      </strong>
                    </div>

                    <div>
                      <span>Historical Support</span>
                      <strong>
                        {formatLabel(
                          data.ai.prediction.historical_support?.status ?? "—"
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>Known Outcomes</span>
                      <strong>
                        {data.ai.prediction.historical_support?.known_outcome_count ?? 0}
                      </strong>
                    </div>
                  </div>

                  <div className="ai-evidence-note">
                    <span className="section-eyebrow">ENGINE TRACE</span>
                    <p>
                      FactoryIQ stellt die AI-Entscheidung nachvollziehbar dar:
                      Signal → Prediction → Root Cause → Decision → Evaluation
                      → Learning. Historische Unterstützung wird nur angezeigt,
                      wenn sie tatsächlich aus der Engine verfügbar ist.
                    </p>
                  </div>
                </div>

                <div className="ai-insights-footer">
                  <div>
                    <span className="section-eyebrow">FACTORYIQ INTELLIGENCE STATUS</span>
                    <strong>
                      {formatLabel(data.ai.operational_signal)}
                      {" · "}
                      {predictionScenarios.length} Prediction-Szenarien
                      {" · "}
                      Decision: {formatLabel(decisionAction)}
                    </strong>
                  </div>

                  <span className="pm-learning-badge">
                    Learning: {formatLabel(learningAction)}
                  </span>
                </div>
              </section>
            ) : (
              <section className="factoryiq-module">
                <div className="module-header">
                  <div>
                    <span className="section-eyebrow">FACTORYIQ MODULE</span>
                    <h1>{activeSection}</h1>
                    <p>Dieser Bereich wird direkt mit der FactoryIQ Intelligence Engine verbunden.</p>
                  </div>
                  <span className="module-live-badge">Engine Connected</span>
                </div>

                <div className="module-placeholder">
                  <span className="section-eyebrow">INTELLIGENCE ENGINE</span>
                  <h2>{activeSection}</h2>
                  <p>Die Modulstruktur ist vorbereitet. Die spezifischen Engine-Daten und Funktionen werden als nächster Schritt integriert.</p>
                </div>
              </section>
            )}
          </div>
        )}

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
          {navItems.map(([icon, label]) => (
            <button
              key={label}
              className={`nav-item ${activeSection === label ? "active" : ""}`}
              onClick={() => setActiveSection(label)}
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
          <span className="search-icon">⌕</span>
          <input
            type="text"
            placeholder="Suche (Maschine, Auftrag, Störung, ...)"
          />
          <span className="search-shortcut">⌘ K</span>
        </div>

        <div className="topbar-right">

          <div className="factory-weather">
            <span className="factory-weather-icon">
              {getWeatherIcon(weather.weatherCode)}
            </span>

            <div className="factory-weather-info">
              <span>SCHWEDT</span>
              <strong>
                {weather.temperature !== null
                  ? `${Math.round(weather.temperature)}°C`
                  : "—"}
              </strong>
            </div>

            <small>
              {getWeatherLabel(weather.weatherCode)}
            </small>
          </div>

          <div className="clock">
            <span>LOCAL TIME</span>
            <strong>
              {currentTime.toLocaleTimeString("de-DE", {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
              })}
            </strong>
            <small>
              {currentTime.toLocaleDateString("de-DE", {
                weekday: "short",
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
              })}
            </small>
          </div>

          <div className="topbar-system">

            <button
              className="system-status-button"
              onClick={(event) => {
                event.stopPropagation();
                setShowSystemPanel(!showSystemPanel);
                setShowNotifications(false);
                setShowUserMenu(false);
              }}
            >
              <span className="system-status-title">
                Alle Systeme
              </span>

              <span className="system-status-line">
                <i className="status-dot" />
                Online
              </span>

              <span className="system-status-site">
                ▦ Werk Schwedt
              </span>
            </button>

            {showSystemPanel && (
              <div className="topbar-popover system-popover">

                <div className="popover-header">
                  <strong>Systemstatus</strong>
                  <span className="online-pill">ONLINE</span>
                </div>

                <div className="system-row">
                  <span>FactoryIQ Engine</span>
                  <strong>Online</strong>
                </div>

                <div className="system-row">
                  <span>AI Intelligence</span>
                  <strong>Online</strong>
                </div>

                <div className="system-row">
                  <span>Factory Data</span>
                  <strong>Connected</strong>
                </div>

                <div className="system-row">
                  <span>Werk Schwedt</span>
                  <strong>Running</strong>
                </div>

                <div className="popover-footer">
                  <span>Last synchronization</span>
                  <strong>{lastUpdate.toLocaleTimeString("de-DE")}</strong>
                </div>

              </div>
            )}

          </div>

          <div className="topbar-action">

            <button
              className={`topbar-icon-button notification-button ${
                showNotifications ? "active" : ""
              }`}
              aria-label="Benachrichtigungen"
              onClick={(event) => {
                event.stopPropagation();
                const nextOpen = !showNotifications;

                setShowNotifications(nextOpen);
                setShowSystemPanel(false);
                setShowUserMenu(false);

                if (nextOpen) {
                  setReadAlarmIds((current) => [
                    ...new Set([
                      ...current,
                      ...data.alarms.alarms.map((alarm) => alarm.id),
                    ]),
                  ]);
                }
              }}
            >
              <span className="bell-icon" aria-hidden="true">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
                  <path d="M10 21h4" />
                </svg>
              </span>
              {unreadAlarmCount > 0 && (
                <b>{unreadAlarmCount > 99 ? "99+" : unreadAlarmCount}</b>
              )}
            </button>

            {showNotifications && (
              <div className="topbar-popover notification-popover">

                <div className="popover-header">
                  <strong>Benachrichtigungen</strong>
                  <span>
                    {unreadAlarmCount > 0
                      ? `${unreadAlarmCount} neu`
                      : "Gelesen"}
                  </span>
                </div>

                {data.alarms.alarms.length > 0 ? (
                  data.alarms.alarms.map((alarm) => (
                    <div
                      className={`notification-item ${
                        alarm.severity === "critical"
                          ? "critical"
                          : alarm.severity === "warning"
                            ? "warning"
                            : "info"
                      }`}
                      key={alarm.id}
                    >
                      <span className="notification-indicator" />

                      <div>
                        <strong>
                          {alarm.severity === "critical"
                            ? "Critical Alarm"
                            : alarm.severity === "warning"
                              ? "Warning"
                              : "Factory Event"}
                        </strong>

                        <small>
                          {alarm.machine_id}
                          {" · "}
                          {alarm.message}
                        </small>

                        <small>
                          {alarm.type}
                          {" · "}
                          {new Date(alarm.timestamp).toLocaleTimeString(
                            "de-DE",
                            {
                              hour: "2-digit",
                              minute: "2-digit",
                            }
                          )}
                        </small>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="notification-empty">
                    <span>✓</span>
                    <div>
                      <strong>Keine aktiven Alarme</strong>
                      <small>FactoryIQ überwacht den Betrieb.</small>
                    </div>
                  </div>
                )}

                <button
                  className="popover-link"
                  onClick={() => {
                    setShowNotifications(false);
                    setActiveSection("Anomalien");
                  }}
                >
                  Alle Ereignisse anzeigen →
                </button>

              </div>
            )}

          </div>

          <div className="topbar-action">

            <button
              className="topbar-icon-button"
              aria-label="Einstellungen"
              onClick={() => {
                setActiveSection("Einstellungen");
                setShowSystemPanel(false);
                setShowNotifications(false);
                setShowUserMenu(false);
              }}
            >
              ⚙
            </button>

          </div>

          <div className="user-menu-wrapper">

            <button
              className="user-avatar-button"
              onClick={(event) => {
                event.stopPropagation();
                setShowUserMenu(!showUserMenu);
                setShowSystemPanel(false);
                setShowNotifications(false);
              }}
            >
              <span className="user-avatar">TB</span>

              <span className="user-meta">
                <strong>Tom Brinkmann</strong>
                <small>FactoryIQ Operator</small>
              </span>

              <span className="user-chevron">
                {showUserMenu ? "⌃" : "⌄"}
              </span>

              <i className="user-online-dot" />
            </button>

            {showUserMenu && (
              <div className="topbar-popover user-popover">

                <div className="user-popover-header">
                  <span className="large-avatar">TB</span>

                  <div>
                    <strong>Tom Brinkmann</strong>
                    <small>FactoryIQ Operator</small>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setActiveSection("Einstellungen");
                    setShowUserMenu(false);
                  }}
                >
                  ⚙ Einstellungen
                </button>

                <button
                  onClick={() => setShowUserMenu(false)}
                >
                  ◉ Operator Status
                  <span className="menu-online">Online</span>
                </button>

                <div className="user-menu-footer">
                  FactoryIQ Enterprise
                  <span>v1.0.0</span>
                </div>

              </div>
            )}

          </div>

        </div>

      </header>

        <div className="content">
          <section className="page-heading">
            <div className="page-heading-main">
              <div>
                <span className="section-eyebrow">FACTORYIQ ENTERPRISE CONTROL CENTER</span>
                <h1>FactoryIQ Command Center</h1>
                <p>Realtime-Transparenz. Höhere Effizienz. Weniger Stillstand.</p>
              </div>

              <div className="command-live-status">
                <span className="command-live-dot" />
                <div>
                  <strong>LIVE ENGINE</strong>
                  <small>
                    Sync {lastUpdate.toLocaleTimeString("de-DE")}
                  </small>
                </div>
              </div>
            </div>

            <div className="heading-actions">
              <div className="time-range-control">
                <button
                  className={`select-button ${
                    showTimeRangeMenu ? "active" : ""
                  }`}
                  onClick={(event) => {
                    event.stopPropagation();
                    setShowTimeRangeMenu(!showTimeRangeMenu);
                  }}
                >
                  {selectedTimeRange}　⌄
                </button>

                {showTimeRangeMenu && (
                  <div className="time-range-menu">
                    <span className="time-range-label">ZEITRAUM</span>

                    {[
                      "Letzte 1 Stunde",
                      "Letzte 6 Stunden",
                      "Letzte 24 Stunden",
                      "Letzte 7 Tage",
                    ].map((range) => (
                      <button
                        key={range}
                        className={
                          selectedTimeRange === range
                            ? "selected"
                            : ""
                        }
                        onClick={() => {
                          setSelectedTimeRange(range);
                          setShowTimeRangeMenu(false);
                        }}
                      >
                        <span>{range}</span>
                        {selectedTimeRange === range && (
                          <span className="time-range-check">✓</span>
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </div>
              <button
                className="primary-button"
                onClick={exportFactoryIQSnapshot}
              >
                ⇩ Exportieren
              </button>
              <div className="command-menu-control">
                <button
                  className={`more-button ${
                    showCommandMenu ? "active" : ""
                  }`}
                  aria-label="Command Center Aktionen"
                  onClick={(event) => {
                    event.stopPropagation();
                    setShowCommandMenu(!showCommandMenu);
                  }}
                >
                  •••
                </button>

                {showCommandMenu && (
                  <div className="command-action-menu">
                    <span className="command-menu-label">
                      COMMAND CENTER
                    </span>

                    <button
                      onClick={() => {
                        setShowCommandMenu(false);
                        loadDashboard();
                      }}
                    >
                      <span>↻</span>
                      <div>
                        <strong>Dashboard aktualisieren</strong>
                        <small>FactoryIQ-Daten sofort synchronisieren</small>
                      </div>
                    </button>

                    <button
                      onClick={() => {
                        setShowCommandMenu(false);
                        exportFactoryIQSnapshot();
                      }}
                    >
                      <span>⇩</span>
                      <div>
                        <strong>Snapshot exportieren</strong>
                        <small>Aktuellen FactoryIQ-Zustand exportieren</small>
                      </div>
                    </button>

                    <button
                      onClick={() => {
                        setShowCommandMenu(false);
                        setActiveSection("Anomalien");
                      }}
                    >
                      <span>△</span>
                      <div>
                        <strong>Anomalien öffnen</strong>
                        <small>Aktuelle AI- und Alarm-Signale anzeigen</small>
                      </div>
                    </button>

                    <button
                      onClick={() => {
                        setShowCommandMenu(false);
                        setShowSystemPanel(true);
                      }}
                    >
                      <span>◉</span>
                      <div>
                        <strong>Systemstatus</strong>
                        <small>Engine- und Werksstatus anzeigen</small>
                      </div>
                    </button>
                  </div>
                )}
              </div>
            </div>
          </section>

          <section className="operational-snapshot">
            <div className="snapshot-header">
              <span className="section-eyebrow">
                OPERATIONAL SNAPSHOT
              </span>
              <span className="snapshot-source">
                FactoryIQ Engine
              </span>
            </div>

            <div className="snapshot-grid">
              <div className="snapshot-item">
                <span>PRODUCTION</span>
                <strong>{productionOutput}</strong>
                <small>
                  target {productionTarget}
                </small>
              </div>

              <div className="snapshot-item">
                <span>MACHINES</span>
                <strong>
                  {runningMachines}/{machineCount}
                </strong>
                <small>running</small>
              </div>

              <div className="snapshot-item">
                <span>ENERGY</span>
                <strong>
                  {data.kpis.energy_consumption}
                </strong>
                <small>{data.kpis.energy_unit}</small>
              </div>

              <div className="snapshot-item">
                <span>ACTIVE ALARMS</span>
                <strong>{alarmCount}</strong>
                <small>
                  {criticalCount} critical · {warningCount} warning
                </small>
              </div>

              <div className="snapshot-item">
                <span>AI EVIDENCE</span>
                <strong>{machineEvidenceCount}</strong>
                <small>
                  {formatLabel(machineEvidenceStrength)}
                </small>
              </div>

              <div className="snapshot-item">
                <span>EVALUATION</span>
                <strong>
                  {evaluationScore.toFixed(2)}
                </strong>
                <small>execution score</small>
              </div>
            </div>
          </section>

          <section className="machine-intelligence-section">
            <div className="section-heading">
              <div>
                <span className="section-eyebrow">MACHINE INTELLIGENCE</span>
                <h2>Machine Intelligence</h2>
              </div>

              <span
                className={`machine-risk-badge ${machineSeverity.toLowerCase()}`}
              >
                {formatLabel(machineSeverity)}
              </span>
            </div>

            <div className="machine-intelligence-grid">
              <div className="machine-main-card">
                <div className="machine-header">
                  <div>
                    <span className="machine-label">MONITORED MACHINE</span>
                    <h3>{machine?.id ?? "Keine Maschine"}</h3>
                    <p>{machine?.name ?? "Unbekannte Maschine"}</p>
                  </div>

                  <span className="machine-status">
                    <i className="online-dot" /> {formatLabel(machineStatus)}
                  </span>
                </div>

                <div className="machine-metrics">
                  <div className="machine-metric sensor-metric">
                    <span>Vibration</span>
                    <strong>
                      {vibrationValue !== null
                        ? `${vibrationValue.toFixed(1)} ${vibrationUnit}`
                        : "Nicht verfügbar"}
                    </strong>
                    {vibrationThreshold !== null && (
                      <small>
                        Threshold {vibrationThreshold.toFixed(1)} {vibrationUnit}
                      </small>
                    )}
                  </div>

                  <div className="machine-metric">
                    <span>Anomaly</span>
                    <strong>{formatLabel(anomalySeverity)}</strong>
                    <small>
                      {anomalySignalCount} Signal
                      {anomalySignalCount === 1 ? "" : "e"}
                    </small>
                  </div>

                  <div className="machine-metric">
                    <span>Confidence</span>
                    <strong>
                      {anomalyConfidence !== null
                        ? `${Math.round(anomalyConfidence * 100)}%`
                        : formatLabel(machineConfidence)}
                    </strong>
                  </div>

                  <div className="machine-metric">
                    <span>Evidence</span>
                    <strong>{machineEvidenceCount}</strong>
                    <small>{formatLabel(machineEvidenceStrength)}</small>
                  </div>
                </div>

                <div className="vibration-gauge">
                  <div className="vibration-gauge-header">
                    <span className="machine-label">VIBRATION RISK</span>

                    <span className="vibration-reading">
                      {vibrationExcessPercent !== null
                        ? `${vibrationExcessPercent >= 0 ? "+" : ""}${vibrationExcessPercent.toFixed(0)}% vs threshold`
                        : "No threshold data"}
                    </span>
                  </div>

                  <div className="vibration-track">
                    <div
                      className="vibration-fill"
                      style={{ width: `${vibrationGaugePercent}%` }}
                    />
                    {vibrationThreshold !== null &&
                      vibrationValue !== null && (
                        <div
                          className="vibration-threshold"
                          style={{ left: "50%" }}
                        />
                      )}
                  </div>

                  <div className="vibration-scale">
                    <span>0</span>
                    <span>
                      Threshold{" "}
                      {vibrationThreshold !== null
                        ? `${vibrationThreshold.toFixed(1)} ${vibrationUnit}`
                        : "—"}
                    </span>
                    <span>
                      {vibrationValue !== null
                        ? `${vibrationValue.toFixed(1)} ${vibrationUnit}`
                        : "—"}
                    </span>
                  </div>
                </div>

                <div className="machine-signals">
                  <span className="machine-label">SUPPORTING SIGNALS</span>

                  <div className="signal-list">
                    {machineSignals.length > 0 ? (
                      machineSignals.map((signal: string) => (
                        <span className="signal-chip" key={signal}>
                          {formatLabel(signal)}
                        </span>
                      ))
                    ) : (
                      <span className="signal-empty">
                        Keine Signale verfügbar
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="machine-decision-card">
                <span className="machine-label">AI DECISION</span>

                <div className="decision-flow">
                  <strong>{formatLabel(decisionType)}</strong>
                  <span>→</span>
                  <strong>{formatLabel(decisionAction)}</strong>
                </div>

                <p>{decisionRationale}</p>

                <div className="machine-learning-block">
                  <span className="machine-label">LEARNING SIGNAL</span>
                  <strong>{formatLabel(learningAction)}</strong>
                  <p>{learningReason}</p>
                </div>
              </div>
            </div>
          </section>

          <section className="ai-decision-workspace-section">
            <div className="section-heading">
              <div>
                <span className="section-eyebrow">
                  AI DECISION WORKSPACE
                </span>
                <h2>AI Operational Reasoning</h2>
              </div>

              <span className="ai-summary-version">
                Engine v{data.version}
              </span>
            </div>

            <div className="decision-trace">

              <div className="decision-trace-step">
                <div className="decision-trace-marker">01</div>

                <div className="decision-trace-card">
                  <div className="decision-trace-icon prediction-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="7" />
                      <circle cx="12" cy="12" r="2" />
                      <path d="M12 2v3" />
                      <path d="M12 19v3" />
                      <path d="M2 12h3" />
                      <path d="M19 12h3" />
                    </svg>
                  </div>

                  <span className="workspace-label">PREDICTION</span>

                  <h3>{predictionTitle}</h3>

                  <p>
                    {predictionDescription ||
                      "Prediction generated from the current operational evidence."}
                  </p>

                  <div className="decision-trace-metrics">
                    <div>
                      <span>CONFIDENCE</span>
                      <strong>
                        {machineConfidence !== "unknown"
                          ? formatLabel(machineConfidence)
                          : "Not available"}
                      </strong>
                    </div>

                    <div>
                      <span>EVIDENCE</span>
                      <strong>
                        {machineEvidenceCount} ·{" "}
                        {formatLabel(machineEvidenceStrength)}
                      </strong>
                    </div>

                    <div>
                      <span>SEVERITY</span>
                      <strong>
                        {formatLabel(anomalySeverity)}
                      </strong>
                    </div>
                  </div>
                </div>
              </div>

              <div className="decision-trace-connector">
                <span>Evidence → Decision</span>
              </div>

              <div className="decision-trace-step">
                <div className="decision-trace-marker">02</div>

                <div className="decision-trace-card decision-trace-decision">
                  <div className="decision-trace-icon decision-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M6 5h12" />
                      <path d="M12 5v5" />
                      <path d="M12 10l-5 5" />
                      <path d="M12 10l5 5" />
                      <circle cx="7" cy="17" r="2" />
                      <circle cx="17" cy="17" r="2" />
                    </svg>
                  </div>

                  <span className="workspace-label">DECISION</span>

                  <div className="workspace-decision-value">
                    <strong>{formatLabel(decisionType)}</strong>
                    <span>→</span>
                    <strong>{formatLabel(decisionAction)}</strong>
                  </div>

                  <p>
                    {decisionRationale ||
                      "No decision rationale available."}
                  </p>

                  <div className="workspace-learning">
                    <span>LEARNING SIGNAL</span>
                    <strong>
                      {formatLabel(learningAction)}
                    </strong>
                  </div>
                </div>
              </div>

              <div className="decision-trace-connector">
                <span>Action → Outcome</span>
              </div>

              <div className="decision-trace-step">
                <div className="decision-trace-marker">03</div>

                <div className="decision-trace-card decision-trace-evaluation">
                  <div className="decision-trace-icon evaluation-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="8" />
                      <path d="m8 12 2.5 2.5L16 9" />
                    </svg>
                  </div>

                  <span className="workspace-label">EVALUATION</span>

                  <div className="workspace-score">
                    {evaluationScore.toFixed(2)}
                  </div>

                  <span className="workspace-evaluation-status">
                    {formatLabel(evaluationStatus)}
                  </span>

                  <div className="workspace-evaluation-row">
                    <span>Action Status</span>
                    <strong>
                      {formatLabel(
                        data.ai.evaluation?.action_status ??
                          "unknown",
                      )}
                    </strong>
                  </div>

                  <div className="workspace-evaluation-row">
                    <span>Learning</span>
                    <strong>
                      {formatLabel(learningAction)}
                    </strong>
                  </div>
                </div>
              </div>

              <div className="decision-trace-connector">
                <span>Evaluation → Learning</span>
              </div>

              <div className="decision-trace-step">
                <div className="decision-trace-marker">04</div>

                <div className="decision-trace-card decision-trace-learning">
                  <div className="decision-trace-icon learning-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M20 11a8 8 0 0 0-14.9-4" />
                      <path d="M4 4v4h4" />
                      <path d="M4 13a8 8 0 0 0 14.9 4" />
                      <path d="M20 20v-4h-4" />
                    </svg>
                  </div>

                  <span className="workspace-label">LEARNING</span>

                  <h3>{formatLabel(learningAction)}</h3>

                  <p>{learningReason}</p>

                  <div className="learning-trace-status">
                    <span>ENGINE FEEDBACK</span>
                    <strong>
                      {formatLabel(learningAction)}
                    </strong>
                  </div>
                </div>
              </div>

            </div>
          </section>

          <section className="operational-timeline-section">
            <div className="section-heading">
              <div>
                <span className="section-eyebrow">
                  AI DECISION TRACE
                </span>
                <h2>Operational Timeline</h2>
              </div>

              <span className="timeline-live-status">
                <i className="online-dot" />
                Live Intelligence
              </span>
            </div>

            <div className="operational-timeline">
              {operationalTimeline.map((item, index) => (
                <div className="timeline-item" key={item.stage}>
                  <div className="timeline-rail">
                    <div className="timeline-node">
                      {index + 1}
                    </div>

                    {index < operationalTimeline.length - 1 && (
                      <div className="timeline-line" />
                    )}
                  </div>

                  <div className="timeline-content">
                    <span className="timeline-stage">
                      {item.stage}
                    </span>

                    <strong>
                      {formatLabel(item.status)}
                    </strong>

                    <p>{item.detail}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

                    <section className="incident-intelligence-section">
            <div className="section-heading">
              <div>
                <span className="section-eyebrow">
                  INCIDENT INTELLIGENCE
                </span>
                <h2>Alarm Correlation</h2>
              </div>

              <span className="ai-summary-version">
                {alarmCount} active incidents
              </span>
            </div>

            <div className="incident-grid">
              <div className="incident-primary-card">
                <div className="incident-header">
                  <div>
                    <span className="machine-label">
                      PRIMARY INCIDENT
                    </span>
                    <strong>
                      {primaryIncident?.id ?? "No active incident"}
                    </strong>
                  </div>

                  <span className="incident-critical-badge">
                    {formatLabel(
                      primaryIncident?.severity ?? "unknown",
                    )}
                  </span>
                </div>

                <div className="incident-machine">
                  <span>Affected machine</span>
                  <strong>
                    {primaryIncident?.machine_id ??
                      machine?.id ?? "Unknown machine"}
                  </strong>
                </div>

                <div className="incident-message">
                  {primaryIncident?.message ??
                    "No active incident message available."}
                </div>

                <div className="incident-correlation">
                  <span className="machine-label">
                    CORRELATED AI SIGNALS
                  </span>

                  <div className="incident-signal-list">
                    {machineSignals.length > 0 ? (
                      machineSignals.map((signal: string) => (
                        <span
                          className="incident-signal"
                          key={signal}
                        >
                          {formatLabel(signal)}
                        </span>
                      ))
                    ) : (
                      <span className="incident-signal">
                        No correlated signal
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="incident-side-card">
                <span className="machine-label">
                  INCIDENT SEVERITY
                </span>

                <strong className="incident-severity-value">
                  {criticalCount > 0
                    ? "Critical"
                    : warningCount > 0
                      ? "Warning"
                      : "Normal"}
                </strong>

                <div className="incident-status-row">
                  <span>Critical</span>
                  <strong>{criticalCount}</strong>
                </div>

                <div className="incident-status-row">
                  <span>Warning</span>
                  <strong>{warningCount}</strong>
                </div>

                <div className="incident-status-row">
                  <span>AI decision</span>
                  <strong>
                    {formatLabel(decisionType)}
                  </strong>
                </div>
              </div>

              <div className="incident-side-card">
                <span className="machine-label">
                  AI RESPONSE
                </span>

                <strong className="incident-response-value">
                  {formatLabel(decisionAction)}
                </strong>

                <p>
                  {decisionRationale ||
                    "AI decision rationale not available."}
                </p>

                <div className="incident-status-row">
                  <span>Evaluation</span>
                  <strong>
                    {evaluationScore.toFixed(2)}
                  </strong>
                </div>
              </div>
            </div>
          </section>

          <section className="historical-intelligence-section">
            <div className="section-heading">
              <div>
                <span className="section-eyebrow">
                  HISTORICAL INTELLIGENCE
                </span>
                <h2>Machine History</h2>
              </div>

              <span className="ai-summary-version">
                {historicalEntryCount} observations
              </span>
            </div>

            <div className="historical-intelligence-grid">
              <div className="history-main-card">
                <div className="history-card-header">
                  <div>
                    <span className="machine-label">
                      MACHINE
                    </span>
                    <strong>
                      {recurringMachineIds[0] ?? "No machine"}
                    </strong>
                  </div>

                  <span className="history-live-badge">
                    Historical
                  </span>
                </div>

                <div className="history-observation-value">
                  {historicalEntryCount}
                </div>

                <span className="history-observation-label">
                  historical observations
                </span>

                <div className="history-bar">
                  <div
                    className="history-bar-running"
                    style={{
                      width: `${Math.min(historicalRunningRate, 100)}%`,
                    }}
                  />
                </div>

                <div className="history-bar-labels">
                  <span>
                    Running {historicalRunning}
                  </span>
                  <span>
                    Warning {historicalWarning}
                  </span>
                </div>
              </div>

              <div className="history-stat-card">
                <span className="machine-label">
                  RUNNING HISTORY
                </span>

                <strong>
                  {historicalRunningRate.toFixed(0)}%
                </strong>

                <span>
                  {historicalRunning} of {historicalEntryCount}
                  observations
                </span>
              </div>

              <div className="history-stat-card">
                <span className="machine-label">
                  WARNING HISTORY
                </span>

                <strong>
                  {historicalWarning}
                </strong>

                <span>
                  recorded observations
                </span>
              </div>

              <div className="history-stat-card">
                <span className="machine-label">
                  MACHINE SIGNAL DENSITY
                </span>

                <strong>
                  {Object.keys(historicalMachineCounts).length}
                </strong>

                <span>
                  machine(s) represented in history
                </span>
              </div>
            </div>
          </section>

          <section className="ai-summary-section">
            <div className="section-heading">
              <div>
                <span className="section-eyebrow">
                  AIHELIXIA INTELLIGENCE
                </span>
                <h2>Intelligence Summary</h2>
              </div>

              <span className="ai-summary-version">
                Engine v{data.version}
              </span>
            </div>

            <div className="ai-summary-grid">
              <div className="ai-summary-item">
                <span>Operational Signal</span>
                <strong>
                  {formatLabel(data.ai.operational_signal)}
                </strong>
              </div>

              <div className="ai-summary-item">
                <span>Prediction</span>
                <strong>{predictionTitle}</strong>
              </div>

              <div className="ai-summary-item">
                <span>Decision</span>
                <strong>
                  {formatLabel(decisionType)}
                  {" → "}
                  {formatLabel(decisionAction)}
                </strong>
              </div>

              <div className="ai-summary-item">
                <span>Learning</span>
                <strong>{formatLabel(learningAction)}</strong>
              </div>

              <div className="ai-summary-item">
                <span>Evaluation</span>
                <strong>
                  {evaluationScore.toFixed(2)}
                </strong>
              </div>

              <div className="ai-summary-item">
                <span>Evidence</span>
                <strong>
                  {machineEvidenceCount} ·{" "}
                  {formatLabel(machineEvidenceStrength)}
                </strong>
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
