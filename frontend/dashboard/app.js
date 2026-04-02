// --- PRODUCTION CLOUD CONFIGURATION ---
const isLocalOrigin = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
const isHttpsOrigin = window.location.protocol === "https:";
let DEFAULT_API = isLocalOrigin ? "http://localhost:8000" : "https://ratio-backend.onrender.com";
let API_BASE_URL = localStorage.getItem('ratio-api-url') || DEFAULT_API;

let cibilGauge;
let currentAuditController = null;

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupNavigation();
    initGauge();
    checkBackendHealth();
    startLocalNodeScanner();
    setupSettings();
    setupAuditFlow();
});

function initApp() {
    document.getElementById('settings-api-url').value = API_BASE_URL;
    document.addEventListener('keydown', (e) => { if (e.key === "Escape") stopLoader(); });
}

// --- CLOUDLESS: LOCAL NODE DISCOVERY (HTTPS AWARE) ---
function startLocalNodeScanner() {
    const nodeStatus = document.getElementById('local-node-status');
    const localCheck = async () => {
        // If we are on HTTPS (GitHub Pages) and trying to reach HTTP (Localhost), browser blocks it.
        if (isHttpsOrigin && API_BASE_URL.startsWith("http://")) {
            nodeStatus.innerText = "LOCAL NODE: HUB SSL MISMATCH";
            nodeStatus.className = "status-badge danger-border";
            return;
        }

        try {
            const controller = new AbortController();
            const tId = setTimeout(() => controller.abort(), 2000);
            const res = await fetch(`${API_BASE_URL}/health`, { mode: 'cors', signal: controller.signal });
            clearTimeout(tId);
            if (res.ok) {
                nodeStatus.innerText = "LOCAL NODE: READY (FREE COMPUTE)";
                nodeStatus.className = "status-badge success-border pulse";
            } else throw new Error();
        } catch {
            nodeStatus.innerText = "LOCAL NODE: OFFLINE";
            nodeStatus.className = "status-badge warning-border";
        }
    };
    localCheck();
    setInterval(localCheck, 10000);
}

// --- CIBIL GAUGE ---
function initGauge() {
    const ctx = document.getElementById('cibilGauge').getContext('2d');
    cibilGauge = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 900],
                backgroundColor: ['#76B900', 'rgba(255, 255, 255, 0.05)'],
                borderWidth: 0,
                cutout: '80%',
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            plugins: { tooltip: { enabled: false }, legend: { display: false } },
            responsive: true, maintainAspectRatio: false
        }
    });
}

function updateGauge(score) {
    cibilGauge.data.datasets[0].data = [score, 900 - score];
    cibilGauge.update();
    animateValue(document.getElementById('ats-score'), 0, score, 1500);
}

// --- AUDIT FLOW (CONCURRENT + TIMEOUT) ---
function setupAuditFlow() {
    const runBtn = document.getElementById('run-audit-btn');
    runBtn.onclick = async () => {
        const modelSelect = document.getElementById('model-select').value;
        const modelName = document.getElementById('model-name').value || modelSelect;

        // 🛡️ SECURITY FIX: Warn user about HTTPS vs HTTP block
        if (isHttpsOrigin && API_BASE_URL.startsWith("http://")) {
            alert("❌ SECURITY BLOCK: GitHub Pages (HTTPS) cannot talk to a Local Backend (HTTP) directly.\n\nFIX:\n1. Click Gear (⚙️) Settings.\n2. Paste an HTTPS Tunnel URL (from ngrok or Localtonet).\n3. Or host the dashboard locally.");
            return;
        }

        if (currentAuditController) currentAuditController.abort();
        currentAuditController = new AbortController();

        startLoader(`Executing Neural Governance Pipeline (Sub-10s Target)...`);

        // Hard Failure Timeout (15 seconds)
        const safetyTimeout = setTimeout(() => {
            if (currentAuditController) {
                currentAuditController.abort();
                stopLoader();
                alert("❌ AUDIT TIMED OUT: Your backend is not responding within 15 seconds. Ensure 'python ratio-sdk/cli.py start' is running.");
            }
        }, 15000);

        try {
            const res = await fetch(`${API_BASE_URL}/audit`, {
                method: 'POST',
                mode: 'cors',
                signal: currentAuditController.signal,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: modelName })
            });

            clearTimeout(safetyTimeout);

            if (!res.ok) throw new Error("CIBIL Engine Connection Failed");

            const data = await res.json();
            updateUI(data);
        } catch (e) {
            if (e.name !== 'AbortError') {
                alert(`❌ Audit Failed: ${e.message}\n\nFIX: Ensure your local node is running on ${API_BASE_URL}`);
            }
        } finally {
            clearTimeout(safetyTimeout);
            stopLoader();
            currentAuditController = null;
        }
    };
}

function updateUI(data) {
    document.getElementById('app-status').innerText = `Audit Speed: ${data.audit_speed} (TURBO C++)`;
    document.getElementById('app-status').className = "status-badge success-border";

    updateGauge(data.ats_score);
    
    const dBadge = document.getElementById('decision');
    dBadge.innerText = data.decision;
    dBadge.style.backgroundColor = getDecisionColor(data.decision);
    document.getElementById('decision-reason').innerText = `Certified ID: ${data.cert_id}. Status: ${data.compliance_status}`;

    if (data.is_certified) document.getElementById('generate-cert-btn').classList.remove('hidden');

    for (const [key, val] of Object.entries(data.ats_dimensions)) {
        const bar = document.getElementById(`bar-${key}`);
        if (bar) bar.style.width = `${val}%`;
    }

    const riskList = document.getElementById('legal-risks-list');
    riskList.innerHTML = '';
    data.legal_risks.forEach(risk => {
        const div = document.createElement('div');
        div.className = 'risk-item danger-border';
        div.innerHTML = `<strong>LAW VIOLERATION:</strong> ${risk}`;
        riskList.appendChild(div);
    });
    
    document.getElementById('penalty-amount').innerText = `₹${extractPenalty(data.penalty_summary)} Cr`;
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
            document.getElementById('current-page-name').innerText = tabId.toUpperCase() + " HUB";
        });
    });
}

// --- UTILS ---
function startLoader(msg) { document.getElementById('loader').classList.remove('hidden'); document.getElementById('loader').querySelector('p').innerText = msg; }
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
    const controller = new AbortController();
    const tId = setTimeout(() => controller.abort(), 2000);
    try {
        const r = await fetch(`${API_BASE_URL}/health`, { signal: controller.signal });
        clearTimeout(tId);
        if (r.ok) { s.innerText = "HUB: ONLINE"; s.className = "status-badge success-border"; }
        else throw new Error();
    } catch { s.innerText = "HUB: OFFLINE"; s.className = "status-badge danger-border"; }
}
function extractPenalty(s) { const m = s.match(/₹(\d+)/); return m ? m[1] : '0'; }
function setupChat() {}
