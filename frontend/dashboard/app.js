// Configuration
const API_URL = "http://localhost:8000/audit";

// Chart Components
let radarChart;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    initChart();
});

// Run Audit Button Listener
document.getElementById('run-audit-btn').addEventListener('click', async () => {
    const modelName = document.getElementById('model-name').value;
    if (!modelName) {
        alert("Please enter a model name.");
        return;
    }

    startLoading();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ model: modelName })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error("Audit failed:", error);
        alert(`Audit failed: ${error.message}. Ensure backend is running and Ollama is available.`);
    } finally {
        stopLoading();
    }
});

// UI Update Functions
function startLoading() {
    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('run-audit-btn').disabled = true;
}

function stopLoading() {
    document.getElementById('loader').classList.add('hidden');
    document.getElementById('run-audit-btn').disabled = false;
}

function updateUI(data) {
    // 1. Update Score
    const scoreEl = document.getElementById('ats-score');
    animateValue(scoreEl, 0, data.ats_score, 1000);

    // 2. Update Decision
    const decisionEl = document.getElementById('decision');
    decisionEl.innerText = data.decision;
    decisionEl.style.backgroundColor = getDecisionColor(data.decision);
    document.getElementById('decision-reason').innerText = data.reason;

    // 3. Update Chart
    const scores = [
        data.dimension_scores.safety,
        data.dimension_scores.bias,
        data.dimension_scores.hallucination,
        data.dimension_scores.security,
        data.dimension_scores.privacy
    ];
    updateChart(scores);

    // 4. Update Legal Risks
    const risksList = document.getElementById('legal-risks-list');
    risksList.innerHTML = '';
    
    if (data.legal_risks && data.legal_risks.length > 0) {
        data.legal_risks.forEach(risk => {
            const item = document.createElement('div');
            item.className = 'risk-item';
            item.innerText = risk;
            risksList.appendChild(item);
        });
        document.getElementById('penalty-amount').innerText = `₹${extractPenalty(data.penalty_summary)} Cr`;
    } else {
        risksList.innerHTML = '<div class="risk-item placeholder">No immediate legal risks detected.</div>';
        document.getElementById('penalty-amount').innerText = '₹0 Cr';
    }

    // 5. Update Recommendations
    const recsList = document.getElementById('recommendations-list');
    recsList.innerHTML = '';
    data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.innerText = rec;
        recsList.appendChild(li);
    });
}

// Helper Functions
function initChart() {
    const ctx = document.getElementById('radarChart').getContext('2d');
    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Safety', 'Bias', 'Hallucination', 'Security', 'Privacy'],
            datasets: [{
                label: 'Governance Score',
                data: [0, 0, 0, 0, 0],
                backgroundColor: 'rgba(118, 185, 0, 0.2)',
                borderColor: '#76B900',
                pointBackgroundColor: '#76B900',
                fill: true
            }]
        },
        options: {
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: { color: '#AAAAAA' },
                    ticks: { display: false },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function updateChart(scores) {
    radarChart.data.datasets[0].data = scores;
    radarChart.update();
}

function getDecisionColor(decision) {
    switch (decision) {
        case 'Regulator Grade': return '#76B900';
        case 'Production Ready': return '#00A4EF';
        case 'Restricted': return '#FDC830';
        case 'Blocked': return '#FF4B2B';
        default: return '#76B900';
    }
}

function extractPenalty(summary) {
    const match = summary.match(/₹(\d+)/);
    return match ? match[1] : '0';
}

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}
