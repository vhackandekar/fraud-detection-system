// Global variables for statistics tracking
let statsUpdateInterval;
let lastTransactionTime = null;

document.addEventListener('DOMContentLoaded', function() {
    // Generate V1-V28 input fields
    const vFieldsContainer = document.getElementById('v-fields');
    for (let i = 1; i <= 28; i++) {
        const div = document.createElement('div');
        div.className = 'form-group';
        div.innerHTML = `
            <label for="v${i}">V${i}:</label>
            <input type="number" id="v${i}" step="0.000001" value="0">
        `;
        vFieldsContainer.appendChild(div);
    }

    // Initial statistics update
    updateStatistics();

    // Set up periodic updates every 5 seconds
    statsUpdateInterval = setInterval(updateStatistics, 5000);

    // Add event listener for form submission
    document.getElementById('transactionForm')
        .addEventListener('submit', submitTransaction);
});

function analyzeTransaction() {
    const transactionData = {
        Amount: parseFloat(document.getElementById('amount').value)
    };

    // Get V1-V28 values
    for (let i = 1; i <= 28; i++) {
        transactionData[`V${i}`] = parseFloat(document.getElementById(`v${i}`).value);
    }

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData)
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    });
}

function displayResults(data) {
    const alertDiv = document.getElementById('fraudAlert');
    const riskScoreDiv = document.getElementById('riskScore');

    if (data.is_fraudulent) {
        alertDiv.className = 'alert fraud';
        alertDiv.textContent = '⚠️ Potential Fraud Detected!';
    } else {
        alertDiv.className = 'alert safe';
        alertDiv.textContent = '✅ Transaction appears safe';
    }

    riskScoreDiv.textContent = `Risk Score: ${data.risk_score.toFixed(4)}`;

    // Create risk score gauge
    const gaugeData = [{
        type: "indicator",
        mode: "gauge+number",
        value: data.risk_score,
        title: { text: "Risk Score" },
        gauge: {
            axis: { range: [0, 1] },
            bar: { color: "darkblue" },
            steps: [
                { range: [0, 0.33], color: "lightgreen" },
                { range: [0.33, 0.66], color: "yellow" },
                { range: [0.66, 1], color: "red" }
            ]
        }
    }];

    Plotly.newPlot('riskGraph', gaugeData);
}

function updateStatistics() {
    fetch('/stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStatsDisplay(data.data);
                updateRiskGauge(data.data.avg_risk_score);
            }
        })
        .catch(error => console.error('Error updating statistics:', error));
}

function updateStatsDisplay(stats) {
    // Update statistics display
    document.querySelectorAll('.stat-item').forEach(item => {
        const key = item.getAttribute('data-stat');
        if (key in stats) {
            const value = stats[key];
            item.querySelector('p').textContent = formatStatValue(key, value);
        }
    });
    
    // Update last refresh time
    document.getElementById('lastUpdate').textContent = 
        `Last Updated: ${new Date().toLocaleTimeString()}`;
}

function formatStatValue(key, value) {
    switch(key) {
        case 'recent_avg_amount':
            return `$${value.toFixed(2)}`;
        case 'recent_fraud_rate':
            return `${value.toFixed(1)}%`;
        default:
            return value.toString();
    }
}

function submitTransaction(event) {
    event.preventDefault();
    
    const amount = document.getElementById('amount').value;
    const data = { Amount: parseFloat(amount) };
    
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResults(data.data);
            lastTransactionTime = new Date();
            // Immediately update statistics after transaction
            updateStatistics();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Cleanup interval when leaving page
window.addEventListener('beforeunload', function() {
    if (statsUpdateInterval) {
        clearInterval(statsUpdateInterval);
    }
});