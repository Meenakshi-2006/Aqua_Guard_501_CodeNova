document.addEventListener("DOMContentLoaded", function () {
    loadDashboardSummary();
    loadOverviewChart();
});

// 1. Fetch summary cards from /api/dashboard/
async function loadDashboardSummary() {
    try {
        const response = await fetch("/api/dashboard/");
        const result = await response.json();

        if (result.success && result.data) {
            const d = result.data;
            document.getElementById("consumption").textContent = d.total_consumption + " L";
            document.getElementById("leaks").textContent = String(d.possible_leaks).padStart(2, "0");
            document.getElementById("sensors").textContent = String(d.active_sensors).padStart(2, "0");
            document.getElementById("loss").textContent = d.estimated_water_loss + " L";
        }
    } catch (error) {
        console.error("Error loading dashboard summary:", error);
    }
}

// 2. Fetch chart data from /api/dashboard/overview (falls back to demo chart if empty)
async function loadOverviewChart() {
    let labels = ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00"];
    let values = [120, 95, 110, 340, 520, 410, 380];

    try {
        const response = await fetch("/api/dashboard/overview");
        const result = await response.json();

        if (result.success && Array.isArray(result.data) && result.data.length > 0) {
            labels = result.data.map(item => item.time || item.label);
            values = result.data.map(item => item.consumption || item.value);
        }
    } catch (error) {
        console.error("Error loading overview chart:", error);
    }

    const ctx = document.getElementById("waterChart");
    if (ctx) {
        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Water Consumption (L/hour)",
                    data: values,
                    borderColor: "#2196f3",
                    backgroundColor: "rgba(33, 150, 243, 0.12)",
                    borderWidth: 2,
                    fill: true,
                    tension: 0.35
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}