// Developer Reference Hub JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
    
    // Set up event listeners
    setupEventListeners();
    
    // Update time and date
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Load saved data
    loadSavedData();
});

function initializeApp() {
    console.log('Developer Reference Hub initialized');
    
    // Initialize Prism for syntax highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
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
    
    // Re-highlight syntax if switching to SQL tab
    if (tabId === 'sql' && typeof Prism !== 'undefined') {
        setTimeout(() => {
            Prism.highlightAll();
        }, 100);
    }
}

function performSearch(tabId, searchTerm) {
    const tabContent = document.getElementById(tabId);
    const items = tabContent.querySelectorAll('.command-item, .query-item, .prompt-item, .project-card');
    
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            item.style.display = 'block';
        } else {
            item.style.display = searchTerm ? 'none' : 'block';
        }
    });
}

function updateDateTime() {
    const now = new Date();
    
    // Update date
    const dateOptions = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString('en-US', dateOptions);
    }
    
    // Update time
    const timeOptions = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    };
    const timeElement = document.getElementById('currentTime');
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString('en-US', timeOptions);
    }
    
    // Update weather (simulated)
    updateWeather();
}

function updateWeather() {
    // Simulate weather data (in a real app, this would come from an API)
    const weatherData = {
        temp: Math.floor(Math.random() * 15) + 15, // 15-30°C
        conditions: ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy'][Math.floor(Math.random() * 4)]
    };
    
    const tempElement = document.getElementById('weatherTemp');
    const descElement = document.getElementById('weatherDesc');
    
    if (tempElement) {
        tempElement.textContent = `${weatherData.temp}°C`;
    }
    if (descElement) {
        descElement.textContent = weatherData.conditions;
    }
}

// Copy functions
function copyCommand(command) {
    copyToClipboard(command, 'Command copied to clipboard!');
}

function copyQuery(query) {
    copyToClipboard(query, 'SQL query copied to clipboard!');
}

function copyPrompt(prompt) {
    copyToClipboard(prompt, 'Cursor prompt copied to clipboard!');
}

function copyToClipboard(text, message) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification(message);
        }).catch(err => {
            console.error('Failed to copy: ', err);
            fallbackCopyTextToClipboard(text, message);
        });
    } else {
        fallbackCopyTextToClipboard(text, message);
    }
}

function fallbackCopyTextToClipboard(text, message) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showNotification(message);
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        showNotification('Failed to copy to clipboard');
    }
    
    document.body.removeChild(textArea);
}

function showNotification(message) {
    // Remove existing notification
    const existingNotification = document.querySelector('.copy-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create new notification
    const notification = document.createElement('div');
    notification.className = 'copy-notification';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Project management functions
function addNewProject() {
    // Simple prompt-based project addition (in a real app, this would open a modal)
    const name = prompt('Enter project name:');
    if (!name) return;
    
    const description = prompt('Enter project description:');
    const githubUrl = prompt('Enter GitHub URL (optional):');
    const liveUrl = prompt('Enter live demo URL (optional):');
    const tech = prompt('Enter technologies (comma-separated):');
    
    const project = {
        name: name,
        description: description || 'No description provided',
        githubUrl: githubUrl || '#',
        liveUrl: liveUrl || '#',
        tech: tech || 'Not specified',
        date: 'Just now'
    };
    
    addProjectToGrid(project);
    saveProject(project);
}

function addProjectToGrid(project) {
    const projectsGrid = document.getElementById('projectsGrid');
    if (!projectsGrid) return;
    
    const projectCard = document.createElement('div');
    projectCard.className = 'project-card';
    projectCard.innerHTML = `
        <div class="project-header">
            <h3>${project.name}</h3>
            <div class="project-status">
                <span class="status-badge active">Active</span>
            </div>
        </div>
        <p class="project-description">${project.description}</p>
        <div class="project-links">
            <a href="${project.githubUrl}" target="_blank" class="project-link">
                <i class="fab fa-github"></i> GitHub
            </a>
            <a href="${project.liveUrl}" class="project-link">
                <i class="fas fa-external-link-alt"></i> Live Demo
            </a>
        </div>
        <div class="project-meta">
            <span class="project-tech">${project.tech}</span>
            <span class="project-date">Updated ${project.date}</span>
        </div>
    `;
    
    projectsGrid.appendChild(projectCard);
}

function saveProject(project) {
    const projects = JSON.parse(localStorage.getItem('devReferenceProjects') || '[]');
    projects.push(project);
    localStorage.setItem('devReferenceProjects', JSON.stringify(projects));
}

function loadSavedData() {
    // Load saved projects
    const projects = JSON.parse(localStorage.getItem('devReferenceProjects') || '[]');
    projects.forEach(project => {
        addProjectToGrid(project);
    });
}

// Utility functions
function refreshData() {
    location.reload();
}

function exportData() {
    const data = {
        projects: JSON.parse(localStorage.getItem('devReferenceProjects') || '[]'),
        exportDate: new Date().toISOString()
    };
    
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'dev-reference-data.json';
    link.click();
    
    showNotification('Data exported successfully!');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + 1-4 to switch tabs
    if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '4') {
        e.preventDefault();
        const tabIndex = parseInt(e.key) - 1;
        const tabs = ['terminal', 'sql', 'cursor', 'projects'];
        if (tabs[tabIndex]) {
            switchTab(tabs[tabIndex]);
        }
    }
    
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const activeTab = document.querySelector('.tab-content.active');
        const searchInput = activeTab.querySelector('input[type="text"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInputs = document.querySelectorAll('input[type="text"]');
        searchInputs.forEach(input => {
            input.value = '';
            performSearch(input.closest('.tab-content').id, '');
        });
    }
});

// Add some sample data on first visit
if (!localStorage.getItem('devReferenceInitialized')) {
    localStorage.setItem('devReferenceInitialized', 'true');
    
    // Add sample projects
    const sampleProjects = [
        {
            name: 'Sample React App',
            description: 'A modern React application with TypeScript and Tailwind CSS.',
            githubUrl: 'https://github.com/sample/react-app',
            liveUrl: 'https://sample-react-app.vercel.app',
            tech: 'React, TypeScript, Tailwind CSS',
            date: '1 week ago'
        }
    ];
    
    localStorage.setItem('devReferenceProjects', JSON.stringify(sampleProjects));
}
