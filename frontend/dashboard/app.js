// --- RATIO AUDIT HUB: NVIDIA-STYLE ENGINE ---
const isLocalOrigin = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
const isHttpsOrigin = window.location.protocol === "https:";
let DEFAULT_API = isLocalOrigin ? "http://localhost:8000" : "https://ratio-backend.onrender.com";
let API_BASE_URL = localStorage.getItem('ratio-api-url') || DEFAULT_API;

let trustGauge;
let auditController = null;

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    logSystem("Pipeline Initialized. Detecting Backend...");
    setupNavigation();
    initTrustGauge();
    checkBackendHealth();
    setupSettings();
    setupAuditFlow();
    startLocalDiscovery();
});

function logSystem(msg, type = "info") {
    const log = document.getElementById('system-log');
    const time = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.style.color = type === "error" ? "#FF4B2B" : "#76B900";
    entry.innerHTML = `[${time}] ${msg}`;
    log.prepend(entry);
    console.log(`[SYSTEM] ${msg}`);
}

// --- GAUGE LOGIC ---
function initTrustGauge() {
    const ctx = document.getElementById('cibilGauge').getContext('2d');
    trustGauge = new Chart(ctx, {
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
            responsive: true, maintainAspectRatio: false,
            animation: { duration: 1500, easing: 'easeOutQuart' }
        }
    });
}

function updateTrustScore(score) {
    trustGauge.data.datasets[0].data = [score, 900 - score];
    trustGauge.update();
    animateValue(document.getElementById('ats-score'), 0, score, 1500);
}

// --- AUDIT EXECUTION (PARALLEL) ---
function setupAuditFlow() {
    const runBtn = document.getElementById('run-audit-btn');
    runBtn.onclick = async () => {
        const modelSelect = document.getElementById('model-select').value;
        const modelName = document.getElementById('model-name').value || modelSelect;

        if (isHttpsOrigin && API_BASE_URL.startsWith("http://")) {
            logSystem("ALARM: SSL Block Detected. Browser prevented HTTPS->HTTP connection.", "error");
            alert("❌ SECURITY BLOCK: GitHub Pages (HTTPS) cannot talk to a Local Backend (HTTP) directly.\n\nUse an HTTPS Tunnel (ngrok) and update settings.");
            return;
        }

        if (auditController) auditController.abort();
        auditController = new AbortController();

        logSystem(`EXECUTING PARALLEL AUDIT FOR: ${modelName}...`);
        startLoader("Neural Pipeline Running...");

        const timeoutId = setTimeout(() => {
            if (auditController) {
                auditController.abort();
                logSystem("ERROR: Audit Pipeline Timeout (15s exceeded).", "error");
                stopLoader();
            }
        }, 15000);

        try {
            const res = await fetch(`${API_BASE_URL}/audit`, {
                method: 'POST',
                mode: 'cors',
                signal: auditController.signal,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: modelName })
            });

            clearTimeout(timeoutId);

            if (!res.ok) throw new Error("Backend Protocol Violation or Server Crash");

            const data = await res.json();
            logSystem(`AUDIT SUCCESS: Trust Score ${data.ats_score} generated in ${data.audit_speed}.`);
            updateUI(data);
        } catch (e) {
            if (e.name !== 'AbortError') {
                logSystem(`CRITICAL ERROR: ${e.message}`, "error");
                alert(`❌ Audit Failed: ${e.message}`);
            }
        } finally {
            clearTimeout(timeoutId);
            stopLoader();
            auditController = null;
        }
    };
}

function updateUI(data) {
    updateTrustScore(data.ats_score);
    
    document.getElementById('decision').innerText = data.decision;
    document.getElementById('decision').style.backgroundColor = getDecisionColor(data.decision);
    document.getElementById('decision-reason').innerText = `Certified Audit ID: ${data.cert_id}`;

    // Dimensions
    for (const [key, val] of Object.entries(data.ats_dimensions)) {
        const bar = document.getElementById(`bar-${key}`);
        if (bar) bar.style.width = `${val}%`;
    }

    if (data.is_certified) document.getElementById('generate-cert-btn').classList.remove('hidden');

    const riskList = document.getElementById('legal-risks-list');
    riskList.innerHTML = '';
    data.legal_risks.forEach(risk => {
        const div = document.createElement('div');
        div.className = 'risk-item-nvidia danger-border';
        div.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${risk}`;
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
            document.getElementById('current-page-name').innerText = tabId.toUpperCase() + " AUDIT";
        });
    });
}

// --- DISCOVERY & HEALTH ---
async function checkBackendHealth() {
    const s = document.getElementById('app-status');
    try {
        const r = await fetch(`${API_BASE_URL}/health`, { mode: 'cors' });
        if (r.ok) {
            s.innerText = "HUB: ONLINE";
            s.className = "status-badge success-glow";
            logSystem(`Connected to Backend Instance: ${API_BASE_URL}`);
        } else throw new Error();
    } catch {
        s.innerText = "HUB: OFFLINE";
        s.className = "status-badge danger-glow";
        logSystem("Backend Instance Disconnected.", "error");
    }
}

function startLocalDiscovery() {
    const nodeStatus = document.getElementById('local-node-status');
    const scan = async () => {
        try {
            const res = await fetch("http://localhost:8000/health", { mode: 'cors' });
            if (res.ok) {
                nodeStatus.innerText = "LOCAL NODE: READY";
                nodeStatus.className = "status-badge success-glow pulse";
            }
        } catch {
            nodeStatus.innerText = "LOCAL NODE: SCANNING...";
            nodeStatus.className = "status-badge warning-glow";
        }
    };
    scan();
    setInterval(scan, 10000);
}

// --- UI UTILS ---
function startLoader(msg) { document.getElementById('loader').classList.remove('hidden'); }
function stopLoader() { document.getElementById('loader').classList.add('hidden'); }
function getDecisionColor(d) {
    if (d.includes('Grade')) return '#76B900';
    if (d.includes('Ready')) return '#00A4EF';
    if (d.includes('Restricted')) return '#FDC830';
    return '#FF4B2B';
}
function animateValue(obj, start, end, duration) {
    let startTime = null;
    const step = (now) => {
        if (!startTime) startTime = now;
        const progress = Math.min((now - startTime) / duration, 1);
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
        logSystem(`Reconfigured Instance to: ${API_BASE_URL}`);
        checkBackendHealth();
    };
}
function extractPenalty(s) { const m = s.match(/₹(\d+)/); return m ? m[1] : '0'; }
