// Personal Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
    
    // Update time every second
    setInterval(updateTime, 1000);
    
    // Load saved data
    loadSavedData();
    
    // Start focus timer if needed
    startFocusTimer();
});

function initializeDashboard() {
    console.log('Personal Dashboard initialized');
    
    // Set initial time
    updateTime();
    
    // Initialize stats
    updateStats();
    
    // Load notes
    loadNotes();
}

function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });
    
    const timeElement = document.getElementById('currentTime');
    if (timeElement) {
        timeElement.textContent = timeString;
    }
}

function updateStats() {
    // Update project count
    const projectCount = document.getElementById('projectCount');
    if (projectCount) {
        projectCount.textContent = '2'; // MCP Demo + Personal Dashboard
    }
    
    // Update task count (from localStorage)
    const taskCount = document.getElementById('taskCount');
    if (taskCount) {
        const tasks = JSON.parse(localStorage.getItem('dashboardTasks') || '[]');
        taskCount.textContent = tasks.length;
    }
    
    // Update focus time
    const focusTime = document.getElementById('focusTime');
    if (focusTime) {
        const savedFocusTime = localStorage.getItem('focusTime') || '0';
        focusTime.textContent = savedFocusTime + 'm';
    }
}

// Quick Actions
function openGitHub() {
    window.open('https://github.com', '_blank');
    addActivity('Opened GitHub', 'fas fa-github');
}

function openCursor() {
    // Try to open Cursor (this might not work in all browsers)
    if (navigator.userAgent.includes('Electron')) {
        // Already in Cursor
        addActivity('Already in Cursor', 'fas fa-code');
    } else {
        // Try to open Cursor app
        addActivity('Attempted to open Cursor', 'fas fa-code');
        alert('Cursor is not available in this browser. Please open it manually.');
    }
}

function openTerminal() {
    addActivity('Opened Terminal', 'fas fa-terminal');
    alert('Terminal opened (simulated)');
}

function startFocus() {
    const focusTime = document.getElementById('focusTime');
    const currentTime = parseInt(focusTime.textContent) || 0;
    const newTime = currentTime + 25; // Add 25 minutes (Pomodoro technique)
    
    focusTime.textContent = newTime + 'm';
    localStorage.setItem('focusTime', newTime.toString());
    
    addActivity('Started focus session (25 min)', 'fas fa-play');
    
    // Show focus notification
    showNotification('Focus session started! 25 minutes of focused work.', 'success');
}

// Activity Management
function addActivity(title, iconClass) {
    const activityList = document.getElementById('activityList');
    if (!activityList) return;
    
    const activityItem = document.createElement('div');
    activityItem.className = 'activity-item';
    activityItem.innerHTML = `
        <div class="activity-icon">
            <i class="${iconClass}"></i>
        </div>
        <div class="activity-content">
            <p class="activity-title">${title}</p>
            <p class="activity-time">Just now</p>
        </div>
    `;
    
    // Add to top of list
    activityList.insertBefore(activityItem, activityList.firstChild);
    
    // Keep only last 10 activities
    const activities = activityList.querySelectorAll('.activity-item');
    if (activities.length > 10) {
        activities[activities.length - 1].remove();
    }
}

// Notes Management
function loadNotes() {
    const notesTextarea = document.getElementById('quickNotes');
    if (notesTextarea) {
        const savedNotes = localStorage.getItem('dashboardNotes') || '';
        notesTextarea.value = savedNotes;
    }
}

function saveNotes() {
    const notesTextarea = document.getElementById('quickNotes');
    if (notesTextarea) {
        localStorage.setItem('dashboardNotes', notesTextarea.value);
        showNotification('Notes saved successfully!', 'success');
        addActivity('Saved notes', 'fas fa-save');
    }
}

function clearNotes() {
    const notesTextarea = document.getElementById('quickNotes');
    if (notesTextarea) {
        if (confirm('Are you sure you want to clear all notes?')) {
            notesTextarea.value = '';
            localStorage.removeItem('dashboardNotes');
            showNotification('Notes cleared!', 'info');
            addActivity('Cleared notes', 'fas fa-trash');
        }
    }
}

// Auto-save notes
document.addEventListener('DOMContentLoaded', function() {
    const notesTextarea = document.getElementById('quickNotes');
    if (notesTextarea) {
        notesTextarea.addEventListener('input', function() {
            // Auto-save after 2 seconds of no typing
            clearTimeout(window.notesTimeout);
            window.notesTimeout = setTimeout(() => {
                localStorage.setItem('dashboardNotes', notesTextarea.value);
            }, 2000);
        });
    }
});

// Load saved data
function loadSavedData() {
    // Load tasks
    const tasks = JSON.parse(localStorage.getItem('dashboardTasks') || '[]');
    updateStats();
    
    // Load focus time
    const focusTime = localStorage.getItem('focusTime') || '0';
    const focusTimeElement = document.getElementById('focusTime');
    if (focusTimeElement) {
        focusTimeElement.textContent = focusTime + 'm';
    }
}

// Focus Timer
let focusInterval;
let focusStartTime;

function startFocusTimer() {
    // Check if there's an active focus session
    const activeFocus = localStorage.getItem('activeFocusSession');
    if (activeFocus) {
        const startTime = parseInt(activeFocus);
        const elapsed = Math.floor((Date.now() - startTime) / 60000); // minutes
        const focusTimeElement = document.getElementById('focusTime');
        if (focusTimeElement) {
            focusTimeElement.textContent = elapsed + 'm';
        }
    }
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        max-width: 300px;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Dashboard Actions
function refreshDashboard() {
    location.reload();
}

function openSettings() {
    showNotification('Settings panel would open here', 'info');
    addActivity('Opened settings', 'fas fa-cog');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + S to save notes
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveNotes();
    }
    
    // Ctrl/Cmd + F to start focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        startFocus();
    }
    
    // Ctrl/Cmd + R to refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        refreshDashboard();
    }
});

// Add some sample data on first visit
if (!localStorage.getItem('dashboardInitialized')) {
    localStorage.setItem('dashboardInitialized', 'true');
    localStorage.setItem('focusTime', '0');
    localStorage.setItem('dashboardTasks', JSON.stringify([
        'Complete MCP integration demo',
        'Set up new project structure',
        'Test dashboard functionality'
    ]));
    
    // Add initial activities
    addActivity('Dashboard initialized', 'fas fa-rocket');
    addActivity('Welcome to your personal dashboard!', 'fas fa-heart');
}
