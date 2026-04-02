// --- TURBO HUB CONFIGURATION ---
let API_BASE_URL = localStorage.getItem('ratio-api-url') || "http://localhost:8000";
let currentAuditData = null;
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
    setupReporting();
});

function initApp() {
    document.getElementById('settings-api-url').value = API_BASE_URL;
    // Auto-recovery: If loader is stuck for some reason, clicking anywhere hides it.
    document.addEventListener('keydown', (e) => { if (e.key === "Escape") stopLoader(); });
}

// --- NAVIGATION ---
function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = link.getAttribute('data-tab');
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            document.querySelectorAll('.tab-pane').forEach(sec => sec.classList.remove('active'));
            const target = document.getElementById(`tab-${tabId}`);
            if (target) target.classList.add('active');
            document.getElementById('current-page-name').innerText = tabId.toUpperCase();
        });
    });
}

// --- TURBO AUDIT ENGINE (PARALLEL) ---
document.getElementById('run-audit-btn').addEventListener('click', async () => {
    const modelName = document.getElementById('model-name').value;
    const turbo = document.getElementById('turbo-mode').checked;
    
    if (!modelName) { alert("Please enter a model name."); return; }

    startLoader(`Initializing ${turbo ? 'Turbo' : 'Standard'} Audit Pipeline...`);

    try {
        const response = await fetch(`${API_BASE_URL}/audit`, {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                model: modelName,
                turbo: turbo 
            })
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({ detail: "CORS/Network Error: Check Backend Settings" }));
            throw new Error(err.detail);
        }

        currentAuditData = await response.json();
        updateDashboardUI(currentAuditData);
    } catch (error) {
        console.error("Audit failed:", error);
        // CRITICAL FIX: Ensure loader disappears on error
        alert(`❌ Audit Error: ${error.message}\n\nFIX:\n1. Open Settings (⚙️) and check API Base URL.\n2. Ensure Ollama/Unsloth is running locally.`);
    } finally {
        stopLoader(); // CRITICAL FIX: Robust state recovery
    }
});

function updateDashboardUI(data) {
    // Topline Metrics (Turbo Timing)
    animateValue(document.getElementById('ats-score'), 0, data.ats_score, 1000);
    animateValue(document.getElementById('ratio-score'), 0, data.ratio_score, 1200);
    
    const statusText = `Aura Hub: ${data.audit_speed || 'Completed'}`;
    document.getElementById('app-status').innerText = statusText;
    document.getElementById('app-status').className = "status-badge success-border";

    document.getElementById('ratio-tests').innerText = `${data.ratio_metrics.passed_tests} / ${data.ratio_metrics.total_tests}`;
    document.getElementById('compliance-status').innerText = data.compliance_status;
    
    const dBadge = document.getElementById('decision');
    dBadge.innerText = data.decision;
    dBadge.style.backgroundColor = getDecisionColor(data.decision);
    document.getElementById('decision-reason').innerText = data.reason;

    updateChart([
        data.ats_dimensions.safety, data.ats_dimensions.bias, 
        data.ats_dimensions.hallucination, data.ats_dimensions.security, 
        data.ats_dimensions.privacy
    ]);

    // Risk Mapping
    const list = document.getElementById('legal-risks-list');
    list.innerHTML = '';
    data.legal_risks.forEach(risk => {
        const div = document.createElement('div');
        div.className = 'risk-item danger-border';
        div.innerHTML = `<strong>LAW VIOLATION:</strong> ${risk}`;
        list.appendChild(div);
    });
}

// --- UTILS & HELPERS ---
function startLoader(msg) { 
    const l = document.getElementById('loader');
    l.querySelector('p').innerText = msg;
    l.classList.remove('hidden'); 
}
function stopLoader() { document.getElementById('loader').classList.add('hidden'); }

function getDecisionColor(d) {
    if (d.includes('Grade')) return '#76B900';
    if (d.includes('Ready')) return '#00A4EF';
    if (d.includes('Restricted')) return '#FDC830';
    return '#FF4B2B';
}
function setupSettings() {
    const modal = document.getElementById('settings-modal');
    document.getElementById('settings-btn').onclick = () => modal.classList.remove('hidden');
    document.getElementById('close-settings').onclick = () => modal.classList.add('hidden');
    document.getElementById('save-settings').onclick = () => {
        API_BASE_URL = document.getElementById('settings-api-url').value.replace(/\/$/, ""); 
        localStorage.setItem('ratio-api-url', API_BASE_URL);
        modal.classList.add('hidden');
        checkBackendHealth();
    };
}
async function checkBackendHealth() {
    const s = document.getElementById('app-status');
    try {
        const r = await fetch(`${API_BASE_URL}/health`, { mode: 'cors' });
        if (r.ok) { s.innerText = "Hub: Connected"; s.className = "status-badge success-border"; }
        else throw new Error();
    } catch { s.innerText = "Hub: Offline"; s.className = "status-badge danger-border"; }
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
// Feature Stubs
function initChart() { /* CHART JS LOGIC */ }
function updateChart(scores) { /* CHART UPDATE */ }
function setupChat() {}
function setupRegistry() {}
function setupMonitoring() {}
function setupReporting() {}
