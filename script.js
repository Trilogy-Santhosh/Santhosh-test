// MCP Integration Demo
document.addEventListener('DOMContentLoaded', function() {
    // Update last updated time
    document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
    
    // Initialize event listeners
    initializeEventListeners();
    
    // Display initial MCP configuration
    displayMCPConfiguration();
});

function initializeEventListeners() {
    // GitHub search functionality
    document.getElementById('searchGithub').addEventListener('click', searchGitHubRepos);
    document.getElementById('githubSearch').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') searchGitHubRepos();
    });
    
    // GitHub repository details
    document.getElementById('getRepoDetails').addEventListener('click', getRepositoryDetails);
    
    // Salesforce functionality
    document.getElementById('getOrgInfo').addEventListener('click', getSalesforceOrgInfo);
    document.getElementById('getUserInfo').addEventListener('click', getSalesforceUserInfo);
}

function displayMCPConfiguration() {
    const config = {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/santhosh.m/Documents/GitHub/Santhosh-test"]
            },
            "awslogs": {
                "url": "https://mcp.csaiautomations.com/awslogs/sse/?token=..."
            },
            "github": {
                "url": "https://mcp.csaiautomations.com/github/sse/?token=..."
            },
            "multidb": {
                "url": "https://mcp.csaiautomations.com/multidb/sse/?token=..."
            },
            "salesforce": {
                "url": "https://mcp.csaiautomations.com/salesforce/sse/?token=..."
            },
            "kayako_tools": {
                "url": "https://mcp.csaiautomations.com/kayako_tools/sse/?token=..."
            },
            "star": {
                "url": "https://mcp.csaiautomations.com/star/sse/?token=..."
            },
            "who_is_on": {
                "url": "https://mcp.csaiautomations.com/who-is-on/sse/?token=..."
            }
        }
    };
    
    console.log('MCP Configuration:', config);
}

// GitHub Integration Functions
async function searchGitHubRepos() {
    const query = document.getElementById('githubSearch').value;
    const resultsContainer = document.getElementById('githubResults');
    const responseContainer = document.getElementById('apiResponse');
    
    if (!query.trim()) {
        showError('Please enter a search query');
        return;
    }
    
    showLoading('searchGithub');
    
    try {
        // Simulate MCP GitHub search (in real implementation, this would call the MCP server)
        const mockResults = await simulateGitHubSearch(query);
        
        displayGitHubResults(mockResults, resultsContainer);
        displayAPIResponse(mockResults, responseContainer, 'GitHub Search');
        
    } catch (error) {
        showError('Failed to search GitHub repositories: ' + error.message);
        console.error('GitHub search error:', error);
    } finally {
        hideLoading('searchGithub');
    }
}

async function getRepositoryDetails() {
    const owner = document.getElementById('repoOwner').value;
    const repoName = document.getElementById('repoName').value;
    const resultsContainer = document.getElementById('repoDetails');
    const responseContainer = document.getElementById('apiResponse');
    
    if (!owner.trim() || !repoName.trim()) {
        showError('Please enter both owner and repository name');
        return;
    }
    
    showLoading('getRepoDetails');
    
    try {
        // Simulate MCP GitHub repository details (in real implementation, this would call the MCP server)
        const mockDetails = await simulateRepositoryDetails(owner, repoName);
        
        displayRepositoryDetails(mockDetails, resultsContainer);
        displayAPIResponse(mockDetails, responseContainer, 'Repository Details');
        
    } catch (error) {
        showError('Failed to get repository details: ' + error.message);
        console.error('Repository details error:', error);
    } finally {
        hideLoading('getRepoDetails');
    }
}

// Salesforce Integration Functions
async function getSalesforceOrgInfo() {
    const resultsContainer = document.getElementById('orgInfo');
    const responseContainer = document.getElementById('apiResponse');
    
    showLoading('getOrgInfo');
    
    try {
        // Simulate MCP Salesforce org info (in real implementation, this would call the MCP server)
        const mockOrgInfo = await simulateSalesforceOrgInfo();
        
        displaySalesforceOrgInfo(mockOrgInfo, resultsContainer);
        displayAPIResponse(mockOrgInfo, responseContainer, 'Salesforce Org Info');
        
    } catch (error) {
        showError('Failed to get Salesforce org info: ' + error.message);
        console.error('Salesforce org info error:', error);
    } finally {
        hideLoading('getOrgInfo');
    }
}

async function getSalesforceUserInfo() {
    const resultsContainer = document.getElementById('userInfo');
    const responseContainer = document.getElementById('apiResponse');
    
    showLoading('getUserInfo');
    
    try {
        // Simulate MCP Salesforce user info (in real implementation, this would call the MCP server)
        const mockUserInfo = await simulateSalesforceUserInfo();
        
        displaySalesforceUserInfo(mockUserInfo, resultsContainer);
        displayAPIResponse(mockUserInfo, responseContainer, 'Salesforce User Info');
        
    } catch (error) {
        showError('Failed to get Salesforce user info: ' + error.message);
        console.error('Salesforce user info error:', error);
    } finally {
        hideLoading('getUserInfo');
    }
}

// Mock Data Functions (simulating MCP responses)
async function simulateGitHubSearch(query) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
        "total_count": 1385,
        "items": [
            {
                "name": "Figma-Context-MCP",
                "full_name": "GLips/Figma-Context-MCP",
                "description": "MCP server to provide Figma layout information to AI coding agents like Cursor",
                "stargazers_count": 10899,
                "language": "TypeScript",
                "html_url": "https://github.com/GLips/Figma-Context-MCP"
            },
            {
                "name": "n8n-mcp",
                "full_name": "czlonkowski/n8n-mcp",
                "description": "A MCP for Claude Desktop / Claude Code / Windsurf / Cursor to build n8n workflows for you",
                "stargazers_count": 7314,
                "language": "TypeScript",
                "html_url": "https://github.com/czlonkowski/n8n-mcp"
            },
            {
                "name": "browser-tools-mcp",
                "full_name": "AgentDeskAI/browser-tools-mcp",
                "description": "Monitor browser logs directly from Cursor and other MCP compatible IDEs.",
                "stargazers_count": 6602,
                "language": "JavaScript",
                "html_url": "https://github.com/AgentDeskAI/browser-tools-mcp"
            }
        ]
    };
}

async function simulateRepositoryDetails(owner, repoName) {
    await new Promise(resolve => setTimeout(resolve, 800));
    
    return {
        "name": repoName,
        "full_name": `${owner}/${repoName}`,
        "description": "MCP server to provide Figma layout information to AI coding agents like Cursor",
        "stargazers_count": 10899,
        "forks_count": 874,
        "language": "TypeScript",
        "created_at": "2025-02-13T02:55:06Z",
        "updated_at": "2025-09-25T11:38:51Z",
        "html_url": `https://github.com/${owner}/${repoName}`,
        "topics": ["ai", "cursor", "figma", "mcp", "typescript"]
    };
}

async function simulateSalesforceOrgInfo() {
    await new Promise(resolve => setTimeout(resolve, 1200));
    
    return {
        "id": "00D000000000000EAA",
        "name": "Trilogy Sales Org",
        "organizationType": "Developer Edition",
        "isSandbox": false,
        "instanceUrl": "https://login.salesforce.com",
        "apiVersion": "60.0",
        "country": "United States",
        "currencyIsoCode": "USD"
    };
}

async function simulateSalesforceUserInfo() {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
        "id": "005000000000000AAA",
        "username": "benji.bizzell@trilogy.com.readonly",
        "firstName": "Benji",
        "lastName": "Bizzell",
        "email": "benji.bizzell@trilogy.com",
        "profile": {
            "name": "System Administrator",
            "id": "00e000000000000AAA"
        },
        "role": {
            "name": "CEO",
            "id": "00E000000000000AAA"
        }
    };
}

// Display Functions
function displayGitHubResults(results, container) {
    if (!results.items || results.items.length === 0) {
        container.innerHTML = '<p>No repositories found.</p>';
        return;
    }
    
    const html = `
        <div class="search-summary">
            <p><strong>Found ${results.total_count} repositories</strong></p>
        </div>
        <div class="repo-list">
            ${results.items.map(repo => `
                <div class="repo-item">
                    <h4><a href="${repo.html_url}" target="_blank">${repo.full_name}</a></h4>
                    <p class="repo-description">${repo.description || 'No description available'}</p>
                    <div class="repo-stats">
                        <span class="stat">⭐ ${repo.stargazers_count.toLocaleString()}</span>
                        <span class="stat">🔧 ${repo.language || 'Unknown'}</span>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    container.innerHTML = html;
}

function displayRepositoryDetails(details, container) {
    const html = `
        <div class="repo-details">
            <h4><a href="${details.html_url}" target="_blank">${details.full_name}</a></h4>
            <p class="repo-description">${details.description || 'No description available'}</p>
            <div class="repo-stats">
                <div class="stat-row">
                    <span class="stat-label">Stars:</span>
                    <span class="stat-value">${details.stargazers_count.toLocaleString()}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Forks:</span>
                    <span class="stat-value">${details.forks_count.toLocaleString()}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Language:</span>
                    <span class="stat-value">${details.language || 'Unknown'}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Created:</span>
                    <span class="stat-value">${new Date(details.created_at).toLocaleDateString()}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Updated:</span>
                    <span class="stat-value">${new Date(details.updated_at).toLocaleDateString()}</span>
                </div>
            </div>
            ${details.topics && details.topics.length > 0 ? `
                <div class="topics">
                    <span class="topics-label">Topics:</span>
                    ${details.topics.map(topic => `<span class="topic-tag">${topic}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `;
    
    container.innerHTML = html;
}

function displaySalesforceOrgInfo(orgInfo, container) {
    const html = `
        <div class="salesforce-info">
            <h4>${orgInfo.name}</h4>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Organization Type:</span>
                    <span class="info-value">${orgInfo.organizationType}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Instance URL:</span>
                    <span class="info-value">${orgInfo.instanceUrl}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">API Version:</span>
                    <span class="info-value">${orgInfo.apiVersion}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Country:</span>
                    <span class="info-value">${orgInfo.country}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Currency:</span>
                    <span class="info-value">${orgInfo.currencyIsoCode}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Sandbox:</span>
                    <span class="info-value">${orgInfo.isSandbox ? 'Yes' : 'No'}</span>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

function displaySalesforceUserInfo(userInfo, container) {
    const html = `
        <div class="salesforce-info">
            <h4>${userInfo.firstName} ${userInfo.lastName}</h4>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Username:</span>
                    <span class="info-value">${userInfo.username}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Email:</span>
                    <span class="info-value">${userInfo.email}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Profile:</span>
                    <span class="info-value">${userInfo.profile.name}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Role:</span>
                    <span class="info-value">${userInfo.role.name}</span>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

function displayAPIResponse(data, container, title) {
    const timestamp = new Date().toLocaleString();
    const response = {
        timestamp: timestamp,
        endpoint: title,
        data: data
    };
    
    container.textContent = JSON.stringify(response, null, 2);
}

// Utility Functions
function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    button.classList.add('loading');
    button.disabled = true;
}

function hideLoading(buttonId) {
    const button = document.getElementById(buttonId);
    button.classList.remove('loading');
    button.disabled = false;
}

function showError(message) {
    // Create a simple error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #fef2f2;
        color: #dc2626;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #fecaca;
        z-index: 1000;
        max-width: 300px;
    `;
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}