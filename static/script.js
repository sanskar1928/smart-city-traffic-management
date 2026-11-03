
async function loadTraffic() {
    try {
        const response = await fetch("/api/traffic");

        if (!response.ok) {
            throw new Error("Failed to fetch traffic");
        }

        const data = await response.json();

        const table = document.getElementById(
            "trafficData"
        );

        table.innerHTML = "";

        data.forEach(item => {
            const row = document.createElement("tr");

            [
                item.road_name,
                item.vehicle_count,
                item.timestamp
            ].forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            table.appendChild(row);
        });
    } catch (error) {
        console.error(error);
    }
}

loadTraffic();
setInterval(loadTraffic, 5000);
