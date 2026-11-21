document.addEventListener("DOMContentLoaded", function () {
    loadDashboardData();
});

async function loadDashboardData() {
    try {
        const sRes = await fetch("/api/sensors");
        const sData = await sRes.json();
        const sensors = sData.sensors || [];

        let totalConsumption = 0;
        let possibleLeaks = 0;
        let activeSensors = 0;
        let estimatedLoss = 0;

        let chartLabels = [];
        let chartValues = [];
        let recentAlerts = [];

        const leakScenarios = ["leak", "burst", "continuous_leak", "burst_leak", "gradual_leak"];

        for (const s of sensors) {
            const rRes = await fetch(`/api/sensors/${encodeURIComponent(s.sensor_id)}/readings`);
            const rData = await rRes.json();
            const readings = rData.readings || [];

            if (readings.length > 0) {
                activeSensors++;
            }

            readings.forEach(r => {
                const flow = Number(r.flow_rate ?? r.flow ?? 0);
                totalConsumption += flow;
            });

            const latest = readings.length > 0 ? readings[readings.length - 1] : null;
            const latestFlow = latest ? Number(latest.flow_rate ?? latest.flow ?? 0) : 0;

            chartLabels.push(`${s.location_id} (${s.sensor_id})`);
            chartValues.push(Number(latestFlow.toFixed(1)));

            const isLeak = leakScenarios.includes(s.scenario) || latestFlow > 110;
            if (isLeak) {
                possibleLeaks++;
                const isBurst = s.scenario === "burst" || s.scenario === "burst_leak" || latestFlow > 150;
                const severity = isBurst ? "High" : "Medium";
                const dailyLoss = isBurst ? Math.round(latestFlow * 6) : Math.round(latestFlow * 4);
                estimatedLoss += dailyLoss;

                recentAlerts.push({
                    location: `${s.location_id} (${s.sensor_id})`,
                    flow: `${latestFlow.toFixed(1)} L/hour`,
                    severity: severity,
                    status: "Pending"
                });
            }
        }

        // Update Top 4 Summary Cards
        const consumptionEl = document.getElementById("consumption");
        const leaksEl = document.getElementById("leaks");
        const sensorsEl = document.getElementById("sensors");
        const lossEl = document.getElementById("loss");

        if (consumptionEl) consumptionEl.textContent = totalConsumption.toFixed(1) + " L";
        if (leaksEl) leaksEl.textContent = String(possibleLeaks).padStart(2, "0");
        if (sensorsEl) sensorsEl.textContent = String(activeSensors).padStart(2, "0");
        if (lossEl) lossEl.textContent = estimatedLoss.toLocaleString() + " L";

        // Render Overview Chart
        const ctx = document.getElementById("waterChart");
        if (ctx) {
            const labelsToUse = chartLabels.length > 0 ? chartLabels : ["No Active Sensors"];
            const valuesToUse = chartValues.length > 0 ? chartValues : [0];

            new Chart(ctx, {
                type: "line",
                data: {
                    labels: labelsToUse,
                    datasets: [{
                        label: "Current Water Flow Rate (L/hour)",
                        data: valuesToUse,
                        borderColor: "#2196f3",
                        backgroundColor: "rgba(33, 150, 243, 0.15)",
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        // Update Recent Leakage Alerts Table
        const alertTbody = document.getElementById("alertTable");
        if (alertTbody) {
            if (recentAlerts.length === 0) {
                alertTbody.innerHTML = `
                    <tr>
                        <td colspan="4" style="text-align:center; color:#15803d;">
                            ${sensors.length === 0
                                ? 'No active sensors yet. Click "Virtual Sensors" -> "+ Load 4 Demo Virtual Sensors" to start!'
                                : '✅ All active virtual sensors operating within normal flow thresholds.'}
                        </td>
                    </tr>`;
            } else {
                alertTbody.innerHTML = "";
                recentAlerts.forEach(a => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td><strong>${a.location}</strong></td>
                        <td>${a.flow}</td>
                        <td style="color:${a.severity === 'High' ? '#dc2626' : '#d97706'}; font-weight:bold;">${a.severity}</td>
                        <td>${a.status}</td>
                    `;
                    alertTbody.appendChild(tr);
                });
            }
        }
    } catch (err) {
        console.error("Dashboard sync error:", err);
    }
}