// Configuration
const API_URL = "http://localhost:8000/audit";

// Chart Components
let radarChart;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    checkBackendHealth();
});

async function checkBackendHealth() {
    const statusEl = document.getElementById('app-status');
    try {
        const res = await fetch("http://localhost:8000/health", { timeout: 2000 });
        if (res.ok) {
            statusEl.innerText = "Backend: Online";
            statusEl.style.color = "#76B900";
            statusEl.style.borderColor = "#76B900";
        } else {
            throw new Error();
        }
    } catch (e) {
        statusEl.innerText = "Backend: Offline (Check FastAPI)";
        statusEl.style.color = "#FF4B2B";
        statusEl.style.borderColor = "#FF4B2B";
    }
}

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
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API Error: ${response.statusText}`);
        }

        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error("Audit failed:", error);
        alert(`❌ Audit Failed: ${error.message}\n\nEnsure:\n1. Backend is running (uvicorn app.main:app)\n2. Ollama is running and model "${modelName}" is pulled.`);
    } finally {
        stopLoading();
    }
});

// UI Update Functions
function startLoading() {
    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('run-audit-btn').disabled = true;
    document.getElementById('app-status').innerText = "Status: Auditing...";
}

function stopLoading() {
    document.getElementById('loader').classList.add('hidden');
    document.getElementById('run-audit-btn').disabled = false;
    checkBackendHealth();
}

function updateUI(data) {
    // 1. Update ATS Score
    const atsScoreEl = document.getElementById('ats-score');
    animateValue(atsScoreEl, 0, data.ats_score, 1000);

    // 2. Update RATIO Score (Original)
    const ratioScoreEl = document.getElementById('ratio-score');
    if (data.ratio_score) {
        animateValue(ratioScoreEl, 0, data.ratio_score, 1200);
        document.getElementById('ratio-tests').innerText = `${data.ratio_metrics.passed_tests} / ${data.ratio_metrics.total_tests}`;
        document.getElementById('compliance-status').innerText = data.ratio_metrics.eligibility;
    }

    // 3. Update Decision
    const decisionEl = document.getElementById('decision');
    decisionEl.innerText = data.decision;
    decisionEl.style.backgroundColor = getDecisionColor(data.decision);
    document.getElementById('decision-reason').innerText = data.reason;

    // 4. Update Chart (ATS Dimensions)
    const scores = [
        data.ats_dimensions.safety,
        data.ats_dimensions.bias,
        data.ats_dimensions.hallucination,
        data.ats_dimensions.security,
        data.ats_dimensions.privacy
    ];
    updateChart(scores);

    // 5. Update Legal Risks
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

    // 6. Update Recommendations
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
                label: 'ATS Dimensions',
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
