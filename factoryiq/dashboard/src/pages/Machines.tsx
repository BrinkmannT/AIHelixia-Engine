import { useEffect, useMemo, useState } from "react";
import { getFactoryDashboard, type FactoryDashboardResponse } from "../services/factoryApi";
import type { MachineStatus } from "../types";

type Filter = "alle" | MachineStatus;

interface MachinesProps {
  onSelectMachine: (machineId: string) => void;
  engineDashboard?: FactoryDashboardResponse | null;
}

export default function Machines({ onSelectMachine, engineDashboard: initialDashboard }: MachinesProps) {
  const [dashboard, setDashboard] = useState<FactoryDashboardResponse | null>(initialDashboard ?? null);
  useEffect(() => {
    if (initialDashboard) return;
    getFactoryDashboard().then(setDashboard).catch(() => {});
  }, [initialDashboard]);
  const [filter, setFilter] = useState<Filter>("alle");
  const [search, setSearch] = useState("");

  const machines = (dashboard?.machines.machines ?? []).map((machine) => ({
    id: machine.id,
    name: machine.name ?? machine.id,
    area: "Werkbereich",
    productionLine: machine.production_line_id ?? "—",
    status: machine.status === "warning" || machine.status === "degraded" ? "warning" : machine.status === "down" || machine.status === "offline" ? "critical" : "normal",
  }));

  const sensors = (dashboard?.sensors.sensors ?? []).map((sensor) => ({
    machineId: String(sensor.machine_id ?? ""),
    type: String(sensor.type ?? ""),
    value: typeof sensor.value === "number" ? sensor.value : undefined,
    unit: String(sensor.unit ?? ""),
  }));

  const maintenancePredictions: Array<{ machineId: string; failureProbability: number }> = [];


  const filteredMachines = useMemo(() => {
    const query = search.trim().toLowerCase();

    return machines.filter((machine) => {
      const matchesFilter =
        filter === "alle" || machine.status === filter;

      const matchesSearch =
        !query ||
        machine.id.toLowerCase().includes(query) ||
        machine.name.toLowerCase().includes(query) ||
        machine.area.toLowerCase().includes(query) ||
        machine.productionLine?.toLowerCase().includes(query);

      return matchesFilter && matchesSearch;
    });
  }, [filter, search]);

  const counts = {
    total: machines.length,
    normal: machines.filter((machine) => machine.status === "normal").length,
    warning: machines.filter((machine) => machine.status === "warning").length,
    critical: machines.filter((machine) => machine.status === "critical").length,
  };

  const getMachineSensor = (machineId: string, type: string) =>
    sensors.find(
      (sensor) => sensor.machineId === machineId && sensor.type === type,
    );

  const getPrediction = (machineId: string) =>
    maintenancePredictions.find(
      (prediction) => prediction.machineId === machineId,
    );

  return (
    <main className="main-content">
      <header className="topbar">
        <div>
          <div className="eyebrow">FACTORYIQ LEITSTAND</div>
          <h1>Maschinen</h1>
          <p>PCK Schwedt · Maschinenübersicht und Zustandsüberwachung</p>
        </div>

        <div className="topbar-actions">
          <div className="live-indicator">
            <span />
            LIVE
          </div>
          <div className="user-avatar">TB</div>
        </div>
      </header>

      <section className="module-header">
        <div>
          <h2>Maschinenübersicht</h2>
          <p>
            Aktueller Zustand, Sensordaten und KI-basierte Ausfallprognosen
          </p>
        </div>

        <div className="module-actions">
          <button className="ghost-button">▣ Bericht erstellen</button>
        </div>
      </section>

      <section className="machine-summary">
        <div className="summary-card">
          <span>Maschinen gesamt</span>
          <strong>{counts.total}</strong>
        </div>

        <div className="summary-card normal">
          <span>Normal</span>
          <strong>{counts.normal}</strong>
        </div>

        <div className="summary-card warning">
          <span>Warnung</span>
          <strong>{counts.warning}</strong>
        </div>

        <div className="summary-card critical">
          <span>Kritisch</span>
          <strong>{counts.critical}</strong>
        </div>
      </section>

      <section className="machine-toolbar">
        <div className="machine-search">
          <span>⌕</span>
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Maschine, Bereich oder Produktionslinie suchen …"
          />
        </div>

        <div className="machine-filters">
          {(["alle", "normal", "warning", "critical"] as Filter[]).map(
            (item) => (
              <button
                key={item}
                className={filter === item ? "active" : ""}
                onClick={() => setFilter(item)}
              >
                {item === "alle"
                  ? "Alle"
                  : item === "normal"
                    ? "Normal"
                    : item === "warning"
                      ? "Warnung"
                      : "Kritisch"}
              </button>
            ),
          )}
        </div>
      </section>

      <section className="machines-table-panel">
        <div className="machines-table-head">
          <span>STATUS</span>
          <span>MASCHINE</span>
          <span>BEREICH</span>
          <span>TEMPERATUR</span>
          <span>SCHWINGUNG</span>
          <span>KI-RISIKO</span>
          <span>AKTION</span>
        </div>

        {filteredMachines.map((machine) => {
          const temperature = getMachineSensor(
            machine.id,
            "temperature",
          );

          const vibration = getMachineSensor(
            machine.id,
            "vibration",
          );

          const prediction = getPrediction(machine.id);

          return (
            <button className="machine-data-row" key={machine.id} onClick={() => onSelectMachine(machine.id)}>
              <span>
                <span className={`status-dot ${machine.status}`} />
              </span>

              <span className="machine-identity">
                <strong>{machine.id}</strong>
                <small>{machine.name}</small>
              </span>

              <span className="table-muted">
                {machine.area}
                <small>{machine.productionLine}</small>
              </span>

              <span className="sensor-value">
                {temperature
                  ? `${temperature.value} ${temperature.unit}`
                  : "—"}
              </span>

              <span className="sensor-value">
                {vibration
                  ? `${vibration.value} ${vibration.unit}`
                  : "—"}
              </span>

              <span>
                {prediction ? (
                  <span
                    className={`risk-value ${
                      prediction.failureProbability >= 70
                        ? "high"
                        : prediction.failureProbability >= 40
                          ? "medium"
                          : "low"
                    }`}
                  >
                    {prediction.failureProbability} %
                  </span>
                ) : (
                  <span className="table-muted">Kein Modell</span>
                )}
              </span>

              <span>
                <span className="row-action">Details →</span>
              </span>
            </button>
          );
        })}

        {filteredMachines.length === 0 && (
          <div className="empty-state">
            <strong>Keine Maschinen gefunden</strong>
            <span>
              Suche oder Statusfilter anpassen.
            </span>
          </div>
        )}
      </section>
    </main>
  );
}
