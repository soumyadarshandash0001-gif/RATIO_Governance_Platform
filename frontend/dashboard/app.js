// --- CONFIGURATION ---
let API_BASE_URL = localStorage.getItem('ratio-api-url') || "http://localhost:8000";

// --- CHART COMPONENTS ---
let radarChart;

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupNavigation();
    initChart();
    checkBackendHealth();
    setupSettings();
    setupChat();
    setupRegistry();
    setupMonitoring();
});

function initApp() {
    // Load persisted settings into modal
    document.getElementById('settings-api-url').value = API_BASE_URL;
}

// --- NAVIGATION (SPA LOGIC) ---
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.tab-pane');
    const pageNameEl = document.getElementById('current-page-name');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = link.getAttribute('data-tab');

            // Update UI
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            sections.forEach(sec => sec.classList.remove('active'));
            document.getElementById(`tab-${tabId}`).classList.add('active');

            // Update Breadcrumb
            pageNameEl.innerText = tabId.charAt(0).toUpperCase() + tabId.slice(1);
        });
    });
}

// --- SYSTEM SETTINGS (CORS FIX) ---
function setupSettings() {
    const settingsBtn = document.getElementById('settings-btn');
    const modal = document.getElementById('settings-modal');
    const closeBtn = document.getElementById('close-settings');
    const saveBtn = document.getElementById('save-settings');

    settingsBtn.onclick = () => modal.classList.remove('hidden');
    closeBtn.onclick = () => modal.classList.add('hidden');
    
    saveBtn.onclick = () => {
        const newUrl = document.getElementById('settings-api-url').value;
        API_BASE_URL = newUrl.replace(/\/$/, ""); // Remove trailing slash
        localStorage.setItem('ratio-api-url', API_BASE_URL);
        modal.classList.add('hidden');
        checkBackendHealth();
        alert(`✅ Configuration Saved: API set to ${API_BASE_URL}`);
    };
}

// --- BACKEND CONNECTIVITY ---
async function checkBackendHealth() {
    const statusEl = document.getElementById('app-status');
    try {
        const res = await fetch(`${API_BASE_URL}/health`, { 
            method: 'GET',
            mode: 'cors',
            headers: { 'Accept': 'application/json' }
        });
        
        if (res.ok) {
            statusEl.innerText = "Backend: Online";
            statusEl.style.color = "#76B900";
            statusEl.style.borderColor = "#76B900";
        } else {
            throw new Error();
        }
    } catch (e) {
        statusEl.innerText = "Backend: Offline (Check Settings)";
        statusEl.style.color = "#FF4B2B";
        statusEl.style.borderColor = "#FF4B2B";
    }
}

// --- UNIFIED AUDIT LOGIC ---
document.getElementById('run-audit-btn').addEventListener('click', async () => {
    const modelName = document.getElementById('model-name').value;
    if (!modelName) { alert("Please enter a model name."); return; }

    startLoader();

    try {
        const response = await fetch(`${API_BASE_URL}/audit`, {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model: modelName })
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({ detail: "Unknown error" }));
            throw new Error(err.detail);
        }

        const data = await response.json();
        updateDashboardUI(data);
    } catch (error) {
        console.error("Audit failed:", error);
        alert(`❌ Unified Audit Failed: ${error.message}\n\nCheck your Settings if using GitHub Pages (CORS/HTTPS).`);
    } finally {
        stopLoader();
    }
});

function updateDashboardUI(data) {
    // Scores
    animateValue(document.getElementById('ats-score'), 0, data.ats_score, 1000);
    animateValue(document.getElementById('ratio-score'), 0, data.ratio_score, 1200);
    
    // Metrics
    document.getElementById('ratio-tests').innerText = `${data.ratio_metrics.passed_tests} / ${data.ratio_metrics.total_tests}`;
    document.getElementById('compliance-status').innerText = data.ratio_metrics.eligibility;
    
    // Decision & Reason
    const decisionEl = document.getElementById('decision');
    decisionEl.innerText = data.decision;
    decisionEl.style.backgroundColor = getDecisionColor(data.decision);
    document.getElementById('decision-reason').innerText = data.reason;

    // Radar Chart
    const scores = [
        data.ats_dimensions.safety, data.ats_dimensions.bias, 
        data.ats_dimensions.hallucination, data.ats_dimensions.security, 
        data.ats_dimensions.privacy
    ];
    updateChart(scores);

    // Legal Risks
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
    }
}

// --- REGISTRY LOGIC ---
function setupRegistry() {
    const form = document.getElementById('register-form');
    form.onsubmit = async (e) => {
        e.preventDefault();
        startLoader();
        try {
            const payload = {
                provider_type: document.getElementById('reg-provider').value,
                model_identifier: document.getElementById('reg-id').value,
                display_name: document.getElementById('reg-name').value,
                max_tokens: parseInt(document.getElementById('reg-tokens').value)
            };
            const res = await fetch(`${API_BASE_URL}/models/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            alert(`✅ ${data.message}\nUUID: ${data.model_uuid}`);
        } catch (e) {
            alert(`❌ Registration failed: ${e.message}`);
        } finally {
            stopLoader();
        }
    };
}

// --- ADVISORY CHAT LOGIC ---
function setupChat() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send');
    const chatBox = document.getElementById('chat-messages');

    sendBtn.onclick = async () => {
        const msg = input.value;
        if (!msg) return;

        // Add user message
        appendMessage('user', msg);
        input.value = '';

        try {
            const res = await fetch(`${API_BASE_URL}/advisory/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ audit_id: "LATEST", question: msg })
            });
            const data = await res.json();
            appendMessage('bot', data.advisory_response);
        } catch (e) {
            appendMessage('bot', "Error connecting to AI Advisor. Ensure backend is online.");
        }
    };

    input.onkeypress = (e) => { if (e.key === 'Enter') sendBtn.click(); };
}

function appendMessage(type, text) {
    const box = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `message ${type}`;
    div.innerText = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

// --- MONITORING LOGIC ---
function setupMonitoring() {
    document.getElementById('run-monitoring').onclick = async () => {
        const uuid = document.getElementById('mon-uuid').value;
        const prevId = document.getElementById('mon-prev-id').value;
        if (!uuid) { alert("Please enter Model UUID"); return; }
        
        startLoader();
        try {
            const res = await fetch(`${API_BASE_URL}/monitoring/re-audit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model_uuid: uuid, previous_audit_id: prevId })
            });
            const data = await res.json();
            document.getElementById('drift-results').classList.remove('hidden');
            document.getElementById('prev-score').innerText = data.previous_score;
            document.getElementById('current-score-mon').innerText = data.new_score;
            document.getElementById('drift-status').innerText = data.drift_detected ? "DRIFT DETECTED" : "SAFE";
            document.getElementById('drift-status').style.color = data.drift_detected ? "#FF4B2B" : "#76B900";
        } catch (e) {
            alert(`❌ Monitoring Failed: ${e.message}`);
        } finally {
            stopLoader();
        }
    };
}

// --- UTILS ---
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
            scales: { r: { angleLines: { color: 'rgba(255, 255, 255, 0.1)' }, grid: { color: 'rgba(255, 255, 255, 0.1)' }, pointLabels: { color: '#AAAAAA' }, ticks: { display: false }, suggestedMin: 0, suggestedMax: 100 } },
            plugins: { legend: { display: false } }
        }
    });
}

function updateChart(scores) { radarChart.data.datasets[0].data = scores; radarChart.update(); }
function startLoader() { document.getElementById('loader').classList.remove('hidden'); }
function stopLoader() { document.getElementById('loader').classList.add('hidden'); }
function getDecisionColor(d) {
    if (d.includes('Grade')) return '#76B900';
    if (d.includes('Ready')) return '#00A4EF';
    if (d.includes('Restricted')) return '#FDC830';
    return '#FF4B2B';
}
function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) window.requestAnimationFrame(step);
    };
    window.requestAnimationFrame(step);
}
function extractPenalty(s) { const m = s.match(/₹(\d+)/); return m ? m[1] : '0'; }
