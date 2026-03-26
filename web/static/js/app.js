// FinCompliance - Financial Compliance Monitoring System
// Multi-page Application Logic

const API_BASE_URL = 'http://localhost:8000';

// State management
let transactionHistory = JSON.parse(localStorage.getItem('transactions')) || [];
let currentPage = 'dashboard';
let complianceRules = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    checkAPIHealth();
    updateDashboard();
    loadTransactionHistory();
    loadComplianceRules();
    setupEventListeners();
    startClock();
    showPage('dashboard');
}

// Event Listeners
function setupEventListeners() {
    const form = document.getElementById('transactionForm');
    if (form) {
        form.addEventListener('submit', handleTransactionSubmit);
    }
}

// Page Navigation
function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('[id$="Page"]').forEach(page => {
        page.classList.add('page-hidden');
    });
    
    // Show selected page
    const pageElement = document.getElementById(pageName + 'Page');
    if (pageElement) {
        pageElement.classList.remove('page-hidden');
    }
    
    // Update navigation active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event?.target?.classList.add('active');
    
    // Update page title
    const titles = {
        dashboard: { title: 'Dashboard', subtitle: 'Real-time compliance monitoring overview' },
        check: { title: 'Check Transaction', subtitle: 'Run compliance check on individual transaction' },
        monitor: { title: 'Live Monitor', subtitle: 'Real-time transaction monitoring' },
        history: { title: 'Transaction History', subtitle: 'View all processed transactions' },
        rules: { title: 'Compliance Rules', subtitle: 'View and configure compliance rules' },
        reports: { title: 'Reports', subtitle: 'Generate and export compliance reports' },
        settings: { title: 'Settings', subtitle: 'System configuration' }
    };
    
    if (titles[pageName]) {
        document.getElementById('pageTitle').textContent = titles[pageName].title;
        document.getElementById('pageSubtitle').textContent = titles[pageName].subtitle;
    }
    
    currentPage = pageName;
    
    // Load page-specific data
    if (pageName === 'history') {
        renderHistoryTable();
    } else if (pageName === 'rules') {
        renderRulesPage();
    } else if (pageName === 'monitor') {
        renderLiveMonitor();
    }
}

// API Health Check
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateAPIStatus(true);
        } else {
            updateAPIStatus(false);
        }
    } catch (error) {
        updateAPIStatus(false);
    }
}

function updateAPIStatus(isOnline) {
    const statusDot = document.getElementById('apiStatusDot');
    const statusText = document.getElementById('apiStatusText');
    
    if (isOnline) {
        statusDot.className = 'status-dot status-online';
        statusText.textContent = 'Connected';
    } else {
        statusDot.className = 'status-dot status-offline';
        statusText.textContent = 'Offline';
    }
}

// Transaction Handling
async function handleTransactionSubmit(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const loadingState = document.getElementById('loadingState');
    const resultsDiv = document.getElementById('complianceResults');
    
    // Show loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    loadingState.style.display = 'block';
    resultsDiv.innerHTML = '';
    
    try {
        const transaction = buildTransactionObject();
        
        const response = await fetch(`${API_BASE_URL}/compliance-check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(transaction)
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        const result = await response.json();
        
        // Store transaction
        const fullTransaction = {
            ...transaction,
            ...result,
            timestamp: new Date().toISOString(),
            id: 'TXN' + Date.now()
        };
        
        transactionHistory.unshift(fullTransaction);
        localStorage.setItem('transactions', JSON.stringify(transactionHistory.slice(0, 100)));
        
        // Display results
        displayComplianceResults(result);
        updateDashboard();
        
        showToast('Transaction processed successfully', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #ef4444;">
                <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p style="font-weight: 500;">Error processing transaction</p>
                <p style="font-size: 0.875rem; margin-top: 0.5rem; color: #9ca3af;">Please ensure the API server is running</p>
            </div>
        `;
        showToast('Error processing transaction', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-search"></i> Check Compliance';
        loadingState.style.display = 'none';
    }
}

function buildTransactionObject() {
    // Get form values
    const transactionType = document.getElementById('transactionType').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const senderCountry = document.getElementById('senderCountry').value;
    const receiverCountry = document.getElementById('receiverCountry').value;
    const beneficiaryName = document.getElementById('beneficiaryName').value;
    const channel = document.getElementById('channel').value;
    
    // High-risk countries list
    const highRiskCountries = ['Iran', 'North Korea', 'Syria', 'Cuba', 'Sudan'];
    
    // Calculate derived fields
    const isHighRiskCountry = highRiskCountries.includes(senderCountry) || highRiskCountries.includes(receiverCountry);
    const isCash = channel === 'ATM';
    const isRoundAmount = amount % 1000 === 0;
    const hour = new Date().getHours();
    const unusualTime = hour < 6 || hour > 22;
    const isOffshore = senderCountry !== receiverCountry;
    
    // Simulate transaction patterns based on history
    const recentTransactions = transactionHistory.slice(0, 10);
    const txnCountLast24h = recentTransactions.length;
    const avgTxnAmount = recentTransactions.length > 0 
        ? recentTransactions.reduce((sum, t) => sum + t.amount, 0) / recentTransactions.length 
        : amount;
    
    return {
        transaction_id: 'TXN' + Date.now(),
        customer_id: 'CUST' + Math.floor(Math.random() * 9000 + 1000),
        amount: amount,
        transaction_type: transactionType,
        location: receiverCountry,
        is_high_risk_country: isHighRiskCountry,
        is_cash: isCash,
        is_round_amount: isRoundAmount,
        unusual_time: unusualTime,
        recipient_new: Math.random() > 0.7,
        txn_count_last_24h: txnCountLast24h,
        avg_txn_amount: avgTxnAmount,
        customer_risk_score: Math.random() * 0.3 + 0.2,
        days_since_last_txn: Math.floor(Math.random() * 30),
        is_offshore: isOffshore,
        velocity_score: txnCountLast24h > 5 ? 0.8 : 0.3,
        hour_of_day: hour,
        day_of_week: new Date().getDay()
    };
}

function displayComplianceResults(result) {
    const resultsDiv = document.getElementById('complianceResults');
    
    const riskColor = result.risk_level === 'HIGH' ? '#ef4444' : 
                     result.risk_level === 'MEDIUM' ? '#f59e0b' : '#10b981';
    
    const badgeClass = result.risk_level === 'HIGH' ? 'badge-high' : 
                      result.risk_level === 'MEDIUM' ? 'badge-medium' : 'badge-low';
    
    let html = `
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; font-weight: 700; color: ${riskColor}; margin-bottom: 0.5rem;">
                ${result.risk_score.toFixed(2)}
            </div>
            <div>
                <span class="badge ${badgeClass}">${result.risk_level} RISK</span>
            </div>
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <div style="font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">
                Transaction ID
            </div>
            <div style="font-size: 0.875rem; color: #6b7280; font-family: monospace;">
                ${result.transaction_id}
            </div>
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <div style="font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">
                Manual Review Required
            </div>
            <div>
                ${result.requires_review 
                    ? '<span class="badge badge-high">YES</span>' 
                    : '<span class="badge badge-low">NO</span>'}
            </div>
        </div>
    `;
    
    if (result.flagged_rules && result.flagged_rules.length > 0) {
        html += `
            <div>
                <div style="font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.75rem;">
                    Flagged Rules (${result.flagged_rules.length})
                </div>
                <div style="max-height: 200px; overflow-y: auto;">
        `;
        
        result.flagged_rules.forEach(rule => {
            html += `
                <div class="rule-item">
                    <div class="rule-name">${rule}</div>
                    <div class="rule-desc">${getRuleDescription(rule)}</div>
                </div>
            `;
        });
        
        html += `</div></div>`;
    } else {
        html += `
            <div style="text-align: center; padding: 1.5rem; background: #f9fafb; border-radius: 6px;">
                <i class="fas fa-check-circle" style="color: #10b981; font-size: 2rem; margin-bottom: 0.5rem;"></i>
                <p style="color: #6b7280; font-size: 0.875rem;">No compliance rules flagged</p>
            </div>
        `;
    }
    
    html += `
        <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb; font-size: 0.75rem; color: #9ca3af;">
            Processed at ${new Date(result.timestamp).toLocaleString()}
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

function getRuleDescription(ruleName) {
    const descriptions = {
        'BSA_LARGE_CASH': 'Large cash transaction exceeds BSA threshold',
        'BSA_STRUCTURING': 'Possible structuring to avoid reporting',
        'FATF_HIGH_RISK': 'Transaction involves high-risk jurisdiction',
        'OFAC_SANCTIONED': 'Sanctioned country or entity detected',
        'AML_VELOCITY': 'Unusual transaction velocity detected',
        'KYC_NEW_CUSTOMER': 'New customer requires enhanced due diligence',
        'PEP_INDICATOR': 'Politically exposed person indicator',
        'SAR_THRESHOLD': 'Suspicious activity report threshold met',
        'CTR_FILING': 'Currency transaction report filing required',
        'WIRE_TRANSFER_RULE': 'International wire transfer monitoring'
    };
    return descriptions[ruleName] || 'Compliance rule triggered';
}

// Dashboard Updates
function updateDashboard() {
    const total = transactionHistory.length;
    const highRisk = transactionHistory.filter(t => t.risk_level === 'HIGH').length;
    const mediumRisk = transactionHistory.filter(t => t.risk_level === 'MEDIUM').length;
    const lowRisk = transactionHistory.filter(t => t.risk_level === 'LOW').length;
    
    document.getElementById('totalTransactions').textContent = total;
    document.getElementById('highRiskCount').textContent = highRisk;
    document.getElementById('mediumRiskCount').textContent = mediumRisk;
    document.getElementById('lowRiskCount').textContent = lowRisk;
    
    renderRecentActivity();
}

function renderRecentActivity() {
    const container = document.getElementById('recentActivityList');
    
    if (transactionHistory.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: #9ca3af;">
                <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <p>No transactions yet</p>
            </div>
        `;
        return;
    }
    
    const recent = transactionHistory.slice(0, 5);
    let html = '<table class="table"><thead><tr><th>Transaction ID</th><th>Amount</th><th>Type</th><th>Risk</th><th>Time</th></tr></thead><tbody>';
    
    recent.forEach(txn => {
        const badgeClass = txn.risk_level === 'HIGH' ? 'badge-high' : 
                          txn.risk_level === 'MEDIUM' ? 'badge-medium' : 'badge-low';
        
        html += `
            <tr>
                <td style="font-family: monospace;">${txn.transaction_id || txn.id}</td>
                <td>$${txn.amount.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td style="text-transform: capitalize;">${txn.transaction_type}</td>
                <td><span class="badge ${badgeClass}">${txn.risk_level}</span></td>
                <td>${new Date(txn.timestamp).toLocaleTimeString()}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

// History Page
function renderHistoryTable() {
    const container = document.getElementById('historyTableContainer');
    
    if (transactionHistory.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: #9ca3af;">
                <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <p>No transaction history</p>
            </div>
        `;
        return;
    }
    
    let html = `
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Amount</th>
                    <th>Type</th>
                    <th>From → To</th>
                    <th>Risk Score</th>
                    <th>Risk Level</th>
                    <th>Review</th>
                    <th>Time</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    transactionHistory.forEach(txn => {
        const badgeClass = txn.risk_level === 'HIGH' ? 'badge-high' : 
                          txn.risk_level === 'MEDIUM' ? 'badge-medium' : 'badge-low';
        
        html += `
            <tr>
                <td style="font-family: monospace; font-size: 0.8125rem;">${txn.transaction_id || txn.id}</td>
                <td style="font-weight: 600;">$${txn.amount.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td style="text-transform: capitalize;">${txn.transaction_type}</td>
                <td style="font-size: 0.8125rem;">${txn.location}</td>
                <td>${txn.risk_score.toFixed(2)}</td>
                <td><span class="badge ${badgeClass}">${txn.risk_level}</span></td>
                <td>${txn.requires_review ? '<span class="badge badge-high">YES</span>' : '<span class="badge badge-low">NO</span>'}</td>
                <td style="font-size: 0.8125rem; color: #6b7280;">${new Date(txn.timestamp).toLocaleString()}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

function clearHistory() {
    if (confirm('Are you sure you want to clear all transaction history?')) {
        transactionHistory = [];
        localStorage.removeItem('transactions');
        updateDashboard();
        renderHistoryTable();
        showToast('Transaction history cleared', 'success');
    }
}

// Rules Page
async function loadComplianceRules() {
    try {
        const response = await fetch(`${API_BASE_URL}/rules`);
        complianceRules = await response.json();
    } catch (error) {
        console.error('Error loading rules:', error);
    }
}

function renderRulesPage() {
    const container = document.getElementById('rulesContent');
    
    if (complianceRules.length === 0) {
        container.innerHTML = '<p style="color: #9ca3af;">Loading rules...</p>';
        loadComplianceRules().then(() => renderRulesPage());
        return;
    }
    
    let html = '<div style="display: grid; gap: 1rem;">';
    
    complianceRules.forEach(rule => {
        html += `
            <div style="padding: 1.25rem; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                    <div>
                        <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">${rule.name}</div>
                        <div style="font-size: 0.8125rem; color: #6b7280;">${rule.description}</div>
                    </div>
                    <span class="badge badge-low">Active</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; font-size: 0.875rem; color: #6b7280;">
                    <div><strong>Category:</strong> ${rule.category}</div>
                    <div><strong>Severity:</strong> ${rule.severity}</div>
                    ${rule.threshold ? `<div><strong>Threshold:</strong> ${rule.threshold}</div>` : ''}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Live Monitor
function renderLiveMonitor() {
    const container = document.getElementById('liveMonitorContent');
    
    const recent = transactionHistory.slice(0, 10);
    
    if (recent.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: #9ca3af;">
                <i class="fas fa-satellite-dish" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <p>Monitoring for new transactions...</p>
                <p style="font-size: 0.875rem; margin-top: 0.5rem;">Submit transactions on the Check page to see them here</p>
            </div>
        `;
        return;
    }
    
    let html = '<div style="display: grid; gap: 1rem;">';
    
    recent.forEach(txn => {
        const riskColor = txn.risk_level === 'HIGH' ? '#ef4444' : 
                         txn.risk_level === 'MEDIUM' ? '#f59e0b' : '#10b981';
        const badgeClass = txn.risk_level === 'HIGH' ? 'badge-high' : 
                          txn.risk_level === 'MEDIUM' ? 'badge-medium' : 'badge-low';
        
        html += `
            <div style="padding: 1.25rem; background: white; border: 1px solid #e5e7eb; border-left: 4px solid ${riskColor}; border-radius: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <div style="font-family: monospace; font-size: 0.875rem; color: #6b7280;">${txn.transaction_id || txn.id}</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-top: 0.25rem;">
                            $${txn.amount.toLocaleString('en-US', {minimumFractionDigits: 2})}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.25rem; font-weight: 700; color: ${riskColor}; margin-bottom: 0.25rem;">
                            ${txn.risk_score.toFixed(2)}
                        </div>
                        <span class="badge ${badgeClass}">${txn.risk_level}</span>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.75rem; font-size: 0.875rem; color: #6b7280;">
                    <div><strong>Type:</strong> ${txn.transaction_type}</div>
                    <div><strong>Location:</strong> ${txn.location}</div>
                    <div><strong>Review:</strong> ${txn.requires_review ? 'Required' : 'Not Required'}</div>
                    <div><strong>Time:</strong> ${new Date(txn.timestamp).toLocaleTimeString()}</div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Reports
function exportCSV() {
    if (transactionHistory.length === 0) {
        showToast('No data to export', 'error');
        return;
    }
    
    let csv = 'Transaction ID,Amount,Type,Location,Risk Score,Risk Level,Review Required,Timestamp\n';
    
    transactionHistory.forEach(txn => {
        csv += `${txn.transaction_id || txn.id},${txn.amount},${txn.transaction_type},${txn.location},${txn.risk_score},${txn.risk_level},${txn.requires_review ? 'YES' : 'NO'},${txn.timestamp}\n`;
    });
    
    downloadFile(csv, 'transactions.csv', 'text/csv');
    showToast('CSV exported successfully', 'success');
}

function exportJSON() {
    if (transactionHistory.length === 0) {
        showToast('No data to export', 'error');
        return;
    }
    
    const json = JSON.stringify(transactionHistory, null, 2);
    downloadFile(json, 'transactions.json', 'application/json');
    showToast('JSON exported successfully', 'success');
}

function generateSummaryReport() {
    const total = transactionHistory.length;
    const highRisk = transactionHistory.filter(t => t.risk_level === 'HIGH').length;
    const mediumRisk = transactionHistory.filter(t => t.risk_level === 'MEDIUM').length;
    const lowRisk = transactionHistory.filter(t => t.risk_level === 'LOW').length;
    const totalAmount = transactionHistory.reduce((sum, t) => sum + t.amount, 0);
    const avgRiskScore = total > 0 ? transactionHistory.reduce((sum, t) => sum + t.risk_score, 0) / total : 0;
    
    const report = `
FINANCIAL COMPLIANCE MONITORING - SUMMARY REPORT
Generated: ${new Date().toLocaleString()}
================================================

TRANSACTION STATISTICS
- Total Transactions: ${total}
- Total Amount: $${totalAmount.toLocaleString('en-US', {minimumFractionDigits: 2})}
- Average Risk Score: ${avgRiskScore.toFixed(3)}

RISK DISTRIBUTION
- High Risk: ${highRisk} (${(highRisk/total*100).toFixed(1)}%)
- Medium Risk: ${mediumRisk} (${(mediumRisk/total*100).toFixed(1)}%)
- Low Risk: ${lowRisk} (${(lowRisk/total*100).toFixed(1)}%)

REVIEW REQUIRED
- Transactions Flagged: ${transactionHistory.filter(t => t.requires_review).length}
- Review Rate: ${(transactionHistory.filter(t => t.requires_review).length/total*100).toFixed(1)}%

================================================
End of Report
    `.trim();
    
    downloadFile(report, 'compliance_summary.txt', 'text/plain');
    showToast('Summary report generated', 'success');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Utility Functions
function loadTransactionHistory() {
    const stored = localStorage.getItem('transactions');
    if (stored) {
        transactionHistory = JSON.parse(stored);
    }
}

function clearAllData() {
    if (confirm('Are you sure you want to clear all data? This cannot be undone.')) {
        transactionHistory = [];
        localStorage.clear();
        updateDashboard();
        showToast('All data cleared', 'success');
        if (currentPage === 'history') {
            renderHistoryTable();
        }
    }
}

function startClock() {
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        document.getElementById('currentTime').textContent = timeString;
    }
    updateClock();
    setInterval(updateClock, 1000);
}

function showToast(message, type = 'info') {
    const colors = {
        success: { bg: '#10b981', text: '#ffffff' },
        error: { bg: '#ef4444', text: '#ffffff' },
        warning: { bg: '#f59e0b', text: '#ffffff' },
        info: { bg: '#3b82f6', text: '#ffffff' }
    };
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <i class="fas ${icons[type]}" style="color: ${colors[type].bg}; font-size: 1.25rem;"></i>
            <span style="font-weight: 500; color: #1f2937;">${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(400px)';
        setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
}

// Auto-refresh dashboard every 5 seconds if on dashboard page
setInterval(() => {
    if (currentPage === 'dashboard') {
        updateDashboard();
    } else if (currentPage === 'monitor') {
        renderLiveMonitor();
    }
}, 5000);

// Check API health every 30 seconds
setInterval(checkAPIHealth, 30000);
