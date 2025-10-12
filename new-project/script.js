// MCP Developer Hub JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
    
    // Set up event listeners
    setupEventListeners();
    
    // Update time and date
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Initialize MCP connections
    initializeMCPConnections();
    
    // Load dashboard data
    loadDashboardData();
});

// Global variables
let mcpConnections = {
    github: { connected: false, data: null },
    database: { connected: false, data: null },
    salesforce: { connected: false, data: null },
    logs: { connected: false, data: null },
    support: { connected: false, data: null },
    team: { connected: false, data: null }
};

function initializeApp() {
    console.log('MCP Developer Hub initialized');
    
    // Initialize Prism for syntax highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
    
    // Initialize Chart.js
    if (typeof Chart !== 'undefined') {
        Chart.defaults.color = '#e2e8f0';
        Chart.defaults.borderColor = '#334155';
    }
}

function setupEventListeners() {
    // Tab navigation
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
    
    // Search functionality
    const searchInputs = document.querySelectorAll('input[type="text"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tabId = this.closest('.tab-content').id;
            performSearch(tabId, searchTerm);
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case '1': e.preventDefault(); switchTab('dashboard'); break;
                case '2': e.preventDefault(); switchTab('github'); break;
                case '3': e.preventDefault(); switchTab('database'); break;
                case '4': e.preventDefault(); switchTab('salesforce'); break;
                case '5': e.preventDefault(); switchTab('logs'); break;
                case '6': e.preventDefault(); switchTab('support'); break;
                case '7': e.preventDefault(); switchTab('team'); break;
                case '8': e.preventDefault(); switchTab('tools'); break;
                case 'k': e.preventDefault(); focusSearch(); break;
            }
        }
        if (e.key === 'Escape') {
            clearSearch();
        }
    });
}

function switchTab(tabId) {
    // Remove active class from all tabs and content
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Add active class to selected tab and content
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(tabId).classList.add('active');
    
    // Load tab-specific data
    loadTabData(tabId);
}

function loadTabData(tabId) {
    switch(tabId) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'github':
            loadGitHubData();
            break;
        case 'database':
            loadDatabaseData();
            break;
        case 'salesforce':
            loadSalesforceData();
            break;
        case 'logs':
            loadLogsData();
            break;
        case 'support':
            loadSupportData();
            break;
        case 'team':
            loadTeamData();
            break;
        case 'tools':
            // Tools tab doesn't need dynamic loading
            break;
    }
}

// MCP Connection Management
function initializeMCPConnections() {
    console.log('Initializing MCP connections...');
    
    // Simulate MCP connection status
        setTimeout(() => {
        updateMCPStatus('github', true);
        updateMCPStatus('database', true);
        updateMCPStatus('salesforce', true);
        updateMCPStatus('logs', true);
        updateMCPStatus('support', true);
        updateMCPStatus('team', true);
    }, 1000);
}

function updateMCPStatus(service, connected) {
    mcpConnections[service].connected = connected;
    const statusElement = document.getElementById(`${service}Status`);
    if (statusElement) {
        statusElement.textContent = connected ? 'Connected' : 'Disconnected';
        statusElement.className = `card-status ${connected ? 'connected' : 'disconnected'}`;
    }
}

// Dashboard Functions
function loadDashboardData() {
    showLoading(true);
    
    // Simulate loading dashboard data
    setTimeout(() => {
        updateDashboardStats();
        updateActivityFeed();
        showLoading(false);
    }, 1500);
}

function updateDashboardStats() {
    // GitHub stats
    document.getElementById('repoCount').textContent = '12';
    document.getElementById('starCount').textContent = '45';
    document.getElementById('forkCount').textContent = '8';
    
    // Database stats
    document.getElementById('dbCount').textContent = '3';
    document.getElementById('tableCount').textContent = '127';
    document.getElementById('queryCount').textContent = '156';
    
    // Salesforce stats
    document.getElementById('leadCount').textContent = '23';
    document.getElementById('oppCount').textContent = '12';
    document.getElementById('contactCount').textContent = '89';
    
    // Logs stats
    document.getElementById('logCount').textContent = '1,247';
    document.getElementById('errorCount').textContent = '3';
    document.getElementById('warningCount').textContent = '12';
    
    // Team stats
    document.getElementById('onlineCount').textContent = '5';
    document.getElementById('busyCount').textContent = '2';
    document.getElementById('awayCount').textContent = '1';
    
    // Support stats
    document.getElementById('ticketCount').textContent = '7';
    document.getElementById('urgentCount').textContent = '1';
    document.getElementById('slaCount').textContent = '95%';
}

function updateActivityFeed() {
    const activityList = document.getElementById('activityList');
    const activities = [
        { icon: 'fas fa-github', text: 'Pushed to repository: mcp-demo', time: '2 minutes ago' },
        { icon: 'fas fa-database', text: 'Executed query on production DB', time: '15 minutes ago' },
        { icon: 'fas fa-cloud', text: 'Updated lead status in Salesforce', time: '1 hour ago' },
        { icon: 'fas fa-headset', text: 'Resolved support ticket #1234', time: '2 hours ago' },
        { icon: 'fas fa-users', text: 'Team meeting completed', time: '3 hours ago' }
    ];
    
    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <i class="${activity.icon}"></i>
            <span>${activity.text}</span>
            <span class="activity-time">${activity.time}</span>
        </div>
    `).join('');
}

// GitHub Functions
function loadGitHubData() {
    showLoading(true);
    
    // Simulate GitHub API call
    setTimeout(() => {
        const repositories = [
            {
                name: 'mcp-demo',
                description: 'Demonstration tool for Model Context Protocol integrations',
                stars: 12,
                forks: 3,
                language: 'JavaScript',
                updated: '2 hours ago',
                private: false
            },
            {
                name: 'dev-reference-hub',
                description: 'Comprehensive reference tool for developers',
                stars: 8,
                forks: 2,
                language: 'HTML',
                updated: '1 day ago',
                private: false
            },
            {
                name: 'ai-chatbot',
                description: 'AI-powered document processing chatbot',
                stars: 15,
                forks: 5,
                language: 'JavaScript',
                updated: '3 days ago',
                private: false
            }
        ];
        
        displayRepositories(repositories);
        showLoading(false);
    }, 1000);
}

function displayRepositories(repositories) {
    const grid = document.getElementById('repositoriesGrid');
    grid.innerHTML = repositories.map(repo => `
        <div class="repository-card">
            <div class="repo-header">
                <h3>${repo.name}</h3>
                <span class="repo-visibility ${repo.private ? 'private' : 'public'}">
                    <i class="fas fa-${repo.private ? 'lock' : 'globe'}"></i>
                    ${repo.private ? 'Private' : 'Public'}
                </span>
            </div>
            <p class="repo-description">${repo.description}</p>
            <div class="repo-stats">
                <span class="repo-stat">
                    <i class="fas fa-star"></i> ${repo.stars}
                </span>
                <span class="repo-stat">
                    <i class="fas fa-code-branch"></i> ${repo.forks}
                </span>
                <span class="repo-language">${repo.language}</span>
            </div>
            <div class="repo-footer">
                <span class="repo-updated">Updated ${repo.updated}</span>
                <div class="repo-actions">
                    <button class="repo-action" onclick="viewRepository('${repo.name}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="repo-action" onclick="cloneRepository('${repo.name}')">
                        <i class="fas fa-clone"></i> Clone
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Database Functions
function loadDatabaseData() {
    showLoading(true);
    
    setTimeout(() => {
        const connections = [
            {
                name: 'Production DB',
                type: 'PostgreSQL',
                host: 'prod-db.company.com',
                status: 'connected',
                tables: 45,
                size: '2.3 GB'
            },
            {
                name: 'Staging DB',
                type: 'MySQL',
                host: 'staging-db.company.com',
                status: 'connected',
                tables: 38,
                size: '1.8 GB'
            },
            {
                name: 'Analytics DB',
                type: 'MongoDB',
                host: 'analytics-db.company.com',
                status: 'disconnected',
                tables: 12,
                size: '890 MB'
            }
        ];
        
        displayDatabaseConnections(connections);
        showLoading(false);
    }, 1000);
}

function displayDatabaseConnections(connections) {
    const container = document.getElementById('databaseConnections');
    container.innerHTML = connections.map(conn => `
        <div class="database-connection">
            <div class="db-header">
                <h3>${conn.name}</h3>
                <span class="db-status ${conn.status}">
                    <i class="fas fa-circle"></i> ${conn.status}
                </span>
            </div>
            <div class="db-info">
                <p><strong>Type:</strong> ${conn.type}</p>
                <p><strong>Host:</strong> ${conn.host}</p>
                <p><strong>Tables:</strong> ${conn.tables}</p>
                <p><strong>Size:</strong> ${conn.size}</p>
            </div>
            <div class="db-actions">
                <button class="db-action" onclick="connectDatabase('${conn.name}')">
                    <i class="fas fa-plug"></i> Connect
                </button>
                <button class="db-action" onclick="browseTables('${conn.name}')">
                    <i class="fas fa-table"></i> Browse
                </button>
            </div>
        </div>
    `).join('');
}

// Salesforce Functions
function loadSalesforceData() {
    showLoading(true);
    
    setTimeout(() => {
        // Update CRM stats
        document.getElementById('sfLeads').textContent = '23';
        document.getElementById('sfOpportunities').textContent = '12';
        document.getElementById('sfContacts').textContent = '89';
        document.getElementById('sfAccounts').textContent = '34';
        
        // Load leads data
        const leads = [
            { name: 'John Smith', company: 'Tech Corp', email: 'john@techcorp.com', status: 'New', value: '$5,000' },
            { name: 'Sarah Johnson', company: 'Innovate Inc', email: 'sarah@innovate.com', status: 'Qualified', value: '$12,000' },
            { name: 'Mike Davis', company: 'StartupXYZ', email: 'mike@startupxyz.com', status: 'Contacted', value: '$8,500' }
        ];
        
        displayLeads(leads);
        createPipelineChart();
        showLoading(false);
    }, 1000);
}

function displayLeads(leads) {
    const table = document.getElementById('leadsTable');
    table.innerHTML = `
        <div class="table-header">
            <div class="table-cell">Name</div>
            <div class="table-cell">Company</div>
            <div class="table-cell">Email</div>
            <div class="table-cell">Status</div>
            <div class="table-cell">Value</div>
        </div>
        ${leads.map(lead => `
            <div class="table-row">
                <div class="table-cell">${lead.name}</div>
                <div class="table-cell">${lead.company}</div>
                <div class="table-cell">${lead.email}</div>
                <div class="table-cell">
                    <span class="status-badge ${lead.status.toLowerCase()}">${lead.status}</span>
                </div>
                <div class="table-cell">${lead.value}</div>
            </div>
        `).join('')}
    `;
}

function createPipelineChart() {
    const ctx = document.getElementById('pipelineChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won'],
            datasets: [{
                data: [5, 3, 2, 1, 1],
                backgroundColor: [
                    '#667eea',
                    '#764ba2',
                    '#f093fb',
                    '#f5576c',
                    '#4ecdc4'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Logs Functions
function loadLogsData() {
    showLoading(true);
    
    setTimeout(() => {
        // Update log stats
        document.getElementById('totalLogs').textContent = '1,247';
        document.getElementById('errorLogs').textContent = '3';
        document.getElementById('warningLogs').textContent = '12';
        document.getElementById('infoLogs').textContent = '1,232';
        
        // Load sample logs
        const logs = [
            { level: 'error', message: 'Database connection failed', timestamp: '2024-01-15 14:30:25', source: 'app-server' },
            { level: 'warning', message: 'High memory usage detected', timestamp: '2024-01-15 14:25:10', source: 'monitoring' },
            { level: 'info', message: 'User login successful', timestamp: '2024-01-15 14:20:45', source: 'auth-service' },
            { level: 'info', message: 'API request processed', timestamp: '2024-01-15 14:15:30', source: 'api-gateway' }
        ];
        
        displayLogs(logs);
        showLoading(false);
    }, 1000);
}

function displayLogs(logs) {
    const container = document.getElementById('logsList');
    container.innerHTML = logs.map(log => `
        <div class="log-entry ${log.level}">
            <div class="log-header">
                <span class="log-level">${log.level.toUpperCase()}</span>
                <span class="log-timestamp">${log.timestamp}</span>
                <span class="log-source">${log.source}</span>
            </div>
            <div class="log-message">${log.message}</div>
        </div>
    `).join('');
}

// Support Functions
function loadSupportData() {
    showLoading(true);
    
    setTimeout(() => {
        const tickets = [
            {
                id: 'TKT-1234',
                title: 'Login issue on mobile app',
                priority: 'High',
                status: 'Open',
                assignee: 'John Doe',
                created: '2 hours ago'
            },
            {
                id: 'TKT-1233',
                title: 'Feature request: Dark mode',
                priority: 'Medium',
                status: 'In Progress',
                assignee: 'Jane Smith',
                created: '1 day ago'
            },
            {
                id: 'TKT-1232',
                title: 'API documentation update needed',
                priority: 'Low',
                status: 'Resolved',
                assignee: 'Mike Johnson',
                created: '3 days ago'
            }
        ];
        
        displaySupportTickets(tickets);
        showLoading(false);
    }, 1000);
}

function displaySupportTickets(tickets) {
    const grid = document.getElementById('ticketsGrid');
    grid.innerHTML = tickets.map(ticket => `
        <div class="ticket-card">
            <div class="ticket-header">
                <h3>${ticket.id}</h3>
                <span class="priority-badge ${ticket.priority.toLowerCase()}">${ticket.priority}</span>
            </div>
            <h4 class="ticket-title">${ticket.title}</h4>
            <div class="ticket-meta">
                <p><strong>Status:</strong> <span class="status-badge ${ticket.status.toLowerCase().replace(' ', '-')}">${ticket.status}</span></p>
                <p><strong>Assignee:</strong> ${ticket.assignee}</p>
                <p><strong>Created:</strong> ${ticket.created}</p>
            </div>
            <div class="ticket-actions">
                <button class="ticket-action" onclick="viewTicket('${ticket.id}')">
                    <i class="fas fa-eye"></i> View
                </button>
                <button class="ticket-action" onclick="updateTicket('${ticket.id}')">
                    <i class="fas fa-edit"></i> Update
                </button>
            </div>
        </div>
    `).join('');
}

// Team Functions
function loadTeamData() {
    showLoading(true);
    
    setTimeout(() => {
        const teamMembers = [
            { name: 'John Doe', role: 'Developer', status: 'online', lastSeen: 'Active now' },
            { name: 'Jane Smith', role: 'Designer', status: 'busy', lastSeen: 'In a meeting' },
            { name: 'Mike Johnson', role: 'DevOps', status: 'away', lastSeen: '2 hours ago' },
            { name: 'Sarah Wilson', role: 'QA Engineer', status: 'online', lastSeen: 'Active now' },
            { name: 'David Brown', role: 'Product Manager', status: 'offline', lastSeen: 'Yesterday' }
        ];
        
        displayTeamMembers(teamMembers);
        showLoading(false);
    }, 1000);
}

function displayTeamMembers(members) {
    const container = document.getElementById('teamStatus');
    container.innerHTML = members.map(member => `
        <div class="team-member">
            <div class="member-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="member-info">
                <h4>${member.name}</h4>
                <p>${member.role}</p>
                <span class="member-status ${member.status}">
                    <i class="fas fa-circle"></i> ${member.lastSeen}
                </span>
            </div>
            <div class="member-actions">
                <button class="member-action" onclick="messageMember('${member.name}')">
                    <i class="fas fa-comment"></i>
                </button>
                <button class="member-action" onclick="callMember('${member.name}')">
                    <i class="fas fa-phone"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Utility Functions
function updateDateTime() {
    const now = new Date();
    const dateElement = document.getElementById('currentDate');
    const timeElement = document.getElementById('currentTime');
    
    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString('en-US', {
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
        });
    }
    
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
}

function performSearch(tabId, searchTerm) {
    // Implement search functionality for each tab
    console.log(`Searching in ${tabId} for: ${searchTerm}`);
}

function focusSearch() {
    const activeTab = document.querySelector('.tab-content.active');
    const searchInput = activeTab.querySelector('input[type="text"]');
    if (searchInput) {
        searchInput.focus();
    }
}

function clearSearch() {
    const searchInputs = document.querySelectorAll('input[type="text"]');
    searchInputs.forEach(input => {
        input.value = '';
    });
}

// Action Functions
function refreshAllData() {
    const currentTab = document.querySelector('.tab-content.active').id;
    loadTabData(currentTab);
}

function refreshGitHubData() {
    loadGitHubData();
}

function refreshDatabaseData() {
    loadDatabaseData();
}

function refreshSalesforceData() {
    loadSalesforceData();
}

function refreshLogsData() {
    loadLogsData();
}

function refreshSupportData() {
    loadSupportData();
}

function refreshTeamData() {
    loadTeamData();
}

function copyCommand(command) {
    navigator.clipboard.writeText(command).then(() => {
        showNotification('Command copied to clipboard!');
    });
}

function exportData() {
    const data = {
        timestamp: new Date().toISOString(),
        mcpConnections: mcpConnections,
        dashboard: {
            github: { repos: 12, stars: 45, forks: 8 },
            database: { connections: 3, tables: 127, queries: 156 },
            salesforce: { leads: 23, opportunities: 12, contacts: 89 }
        }
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `mcp-hub-data-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showNotification('Data exported successfully!');
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Placeholder functions for future MCP integration
function viewRepository(repoName) {
    showNotification(`Viewing repository: ${repoName}`);
}

function cloneRepository(repoName) {
    showNotification(`Cloning repository: ${repoName}`);
}

function addDatabaseConnection() {
    showNotification('Add database connection dialog would open here');
}

function connectDatabase(dbName) {
    showNotification(`Connecting to database: ${dbName}`);
}

function browseTables(dbName) {
    showNotification(`Browsing tables in: ${dbName}`);
}

function executeQuery() {
    const query = document.getElementById('sqlQuery').value;
    if (query.trim()) {
        showNotification('Executing query...');
        // Simulate query execution
        setTimeout(() => {
            document.getElementById('queryResults').innerHTML = `
                <div class="query-result">
                    <h4>Query Results</h4>
                    <p>Query executed successfully. Results would be displayed here.</p>
                </div>
            `;
        }, 1000);
    }
}

function formatQuery() {
    const query = document.getElementById('sqlQuery').value;
    if (query.trim()) {
        showNotification('Query formatted!');
    }
}

function createNewTicket() {
    showNotification('New ticket creation dialog would open here');
}

function viewTicket(ticketId) {
    showNotification(`Viewing ticket: ${ticketId}`);
}

function updateTicket(ticketId) {
    showNotification(`Updating ticket: ${ticketId}`);
}

function messageMember(memberName) {
    showNotification(`Messaging ${memberName}`);
}

function callMember(memberName) {
    showNotification(`Calling ${memberName}`);
}