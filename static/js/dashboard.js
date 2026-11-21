
// =====================================
// AQUAGUARD - DASHBOARD JAVASCRIPT
// =====================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("AquaGuard Dashboard Loaded Successfully!");

    // ---------------------------------
    // WATER CONSUMPTION CHART
    // ---------------------------------

    const chartCanvas = document.getElementById("waterChart");

    if (chartCanvas && typeof Chart !== "undefined") {

        const ctx = chartCanvas.getContext("2d");

        const waterChart = new Chart(ctx, {

            type: "line",

            data: {
                labels: [
                    "6 AM",
                    "8 AM",
                    "10 AM",
                    "12 PM",
                    "2 PM",
                    "4 PM",
                    "6 PM",
                    "8 PM"
                ],

                datasets: [{
                    label: "Water Consumption (Litres)",

                    data: [
                        120,
                        180,
                        150,
                        250,
                        220,
                        300,
                        270,
                        350
                    ],

                    borderColor: "#2196f3",

                    backgroundColor: "rgba(33, 150, 243, 0.15)",

                    borderWidth: 3,

                    fill: true,

                    tension: 0.4,

                    pointRadius: 5,

                    pointBackgroundColor: "#2196f3",

                    pointBorderColor: "#ffffff",

                    pointBorderWidth: 2
                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: true,
                        position: "top"
                    },

                    tooltip: {
                        enabled: true
                    }
                },

                scales: {

                    y: {
                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "Consumption (Litres)"
                        }
                    },

                    x: {
                        title: {
                            display: true,
                            text: "Time"
                        }
                    }
                }
            }

        });

    } else {
        console.error(
            "Water chart canvas or Chart.js library not found."
        );
    }

});
