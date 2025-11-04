// Global variables
let uploadedDocuments = [];
let documentContent = '';
let isProcessing = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up chat input
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
    chatInput.addEventListener('keypress', handleKeyPress);
    }
}

// File upload handling
function handleFileUpload(event) {
    const files = Array.from(event.target.files);
    processFiles(files);
}

// Drag and drop handling
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.style.borderColor = '#5a67d8';
    event.currentTarget.style.backgroundColor = '#f0f4ff';
}

function handleDragLeave(event) {
    event.currentTarget.style.borderColor = '#667eea';
    event.currentTarget.style.backgroundColor = '#f8f9ff';
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.style.borderColor = '#667eea';
    event.currentTarget.style.backgroundColor = '#f8f9ff';
    
    const files = Array.from(event.dataTransfer.files);
    processFiles(files);
}

// Process uploaded files
async function processFiles(files) {
    if (isProcessing) return;
    
    const validFiles = files.filter(file => 
        file.type === 'text/plain' || 
        file.type === 'application/pdf' ||
        file.name.toLowerCase().endsWith('.txt') ||
        file.name.toLowerCase().endsWith('.pdf')
    );
    
    if (validFiles.length === 0) {
        alert('Please upload only PDF or TXT files.');
        return;
    }
    
    showLoading(true);
    isProcessing = true;
    
    try {
        for (const file of validFiles) {
            const content = await readFileContent(file);
            uploadedDocuments.push({
                name: file.name,
                size: file.size,
                content: content,
                type: file.type
            });
        }
        
        // Combine all document content
        documentContent = uploadedDocuments.map(doc => doc.content).join('\n\n');
        
        // Show chat interface
        showChatInterface();
        updateDocumentCount();
        
        // Add welcome message with document info
        let message = `I've successfully processed ${uploadedDocuments.length} document(s). `;
        
        // Check if any PDFs were processed
        const pdfCount = uploadedDocuments.filter(doc => doc.type === 'application/pdf' || doc.name.toLowerCase().endsWith('.pdf')).length;
        if (pdfCount > 0) {
            message += `Including ${pdfCount} PDF file(s) with improved text extraction. `;
        }
        
        message += "You can now ask me questions about the content!";
        addMessage('bot', message);
        
    } catch (error) {
        console.error('Error processing files:', error);
        alert('Error processing files. Please try again.');
    } finally {
        showLoading(false);
        isProcessing = false;
    }
}

// Read file content
function readFileContent(file) {
    return new Promise(async (resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = async function(e) {
            const content = e.target.result;
            
            if (file.type === 'text/plain' || file.name.toLowerCase().endsWith('.txt')) {
                resolve(content);
            } else if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
                try {
                    // Extract text from PDF content
                    const extractedText = await extractTextFromPDF(content);
                    resolve(extractedText);
                } catch (error) {
                    reject(error);
                }
            } else {
                reject(new Error('Unsupported file type'));
            }
        };
        
        reader.onerror = function() {
            reject(new Error('Error reading file'));
        };
        
        if (file.type === 'text/plain' || file.name.toLowerCase().endsWith('.txt')) {
            reader.readAsText(file);
        } else if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
            // Read as ArrayBuffer for PDF processing
            reader.readAsArrayBuffer(file);
        } else {
            reject(new Error('Unsupported file type'));
        }
    });
}

// Extract text from PDF content using PDF.js
async function extractTextFromPDF(arrayBuffer) {
    try {
        // Use PDF.js for better text extraction
        if (typeof pdfjsLib !== 'undefined') {
            const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
            let fullText = '';
            
            // Extract text from all pages
            for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                const page = await pdf.getPage(pageNum);
                const textContent = await page.getTextContent();
                
                // Combine all text items
                const pageText = textContent.items
                    .map(item => item.str)
                    .join(' ')
                    .trim();
                
                if (pageText) {
                    fullText += pageText + '\n';
                }
            }
            
            if (fullText.trim()) {
                return fullText.trim();
            }
        }
        
        // Fallback to manual extraction if PDF.js is not available
        return extractTextFromPDFManual(arrayBuffer);
        
    } catch (error) {
        console.error('Error extracting PDF text with PDF.js:', error);
        // Fallback to manual extraction
        return extractTextFromPDFManual(arrayBuffer);
    }
}

// Manual PDF text extraction (fallback)
function extractTextFromPDFManual(arrayBuffer) {
    try {
        // Convert ArrayBuffer to Uint8Array
        const uint8Array = new Uint8Array(arrayBuffer);
        
        // Convert to string
        let text = '';
        for (let i = 0; i < uint8Array.length; i++) {
            text += String.fromCharCode(uint8Array[i]);
        }
        
        // Basic PDF text extraction using regex patterns
        const textMatches = text.match(/BT\s+.*?ET/g);
        if (textMatches) {
            let extractedText = '';
            textMatches.forEach(match => {
                // Extract text between parentheses
                const textInParens = match.match(/\(([^)]+)\)/g);
                if (textInParens) {
                    textInParens.forEach(textMatch => {
                        const cleanText = textMatch.replace(/[()]/g, '').trim();
                        if (cleanText && cleanText.length > 1 && !cleanText.match(/^[0-9\s]+$/)) {
                            extractedText += cleanText + ' ';
                        }
                    });
                }
            });
            
            if (extractedText.trim()) {
                return extractedText.trim();
            }
        }
        
        // Fallback: try to extract readable text using a different approach
        const readableText = extractReadableText(text);
        if (readableText.trim()) {
            return readableText.trim();
        }
        
        // If no text could be extracted, return a helpful message
        return "PDF content could not be extracted. This might be an image-based PDF or a complex document. Please try uploading a text-based PDF or convert it to a TXT file first.";
        
    } catch (error) {
        console.error('Error extracting PDF text manually:', error);
        return "Error processing PDF file. Please try uploading a different PDF or convert it to a TXT file.";
    }
}

// Extract readable text from PDF content
function extractReadableText(text) {
    // Remove PDF structure markers
    let cleanText = text
        .replace(/\/[A-Za-z]+\s+[0-9]+\s+0\s+R/g, '') // Remove references
        .replace(/[0-9]+\s+0\s+obj/g, '') // Remove object markers
        .replace(/endobj/g, '') // Remove endobj markers
        .replace(/stream[\s\S]*?endstream/g, '') // Remove stream content
        .replace(/BT[\s\S]*?ET/g, '') // Remove text objects
        .replace(/[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+/g, '') // Remove coordinates
        .replace(/[0-9]+\.[0-9]+\s+[0-9]+\.[0-9]+\s+[0-9]+\.[0-9]+\s+[0-9]+\.[0-9]+/g, '') // Remove more coordinates
        .replace(/[0-9]+\s+[0-9]+\s+[0-9]+/g, '') // Remove triplets
        .replace(/[0-9]+\s+[0-9]+/g, '') // Remove pairs
        .replace(/[0-9]+/g, '') // Remove single numbers
        .replace(/[^\w\s.,!?;:()-]/g, ' ') // Remove special characters except basic punctuation
        .replace(/\s+/g, ' ') // Normalize whitespace
        .trim();
    
    // Extract sentences that look like real text
    const sentences = cleanText.split(/[.!?]+/).filter(sentence => {
        const trimmed = sentence.trim();
        return trimmed.length > 10 && 
               trimmed.split(' ').length > 3 && 
               !trimmed.match(/^[0-9\s]+$/) &&
               trimmed.match(/[a-zA-Z]/);
    });
    
    return sentences.join('. ').trim();
}

// Process pasted text
function processText() {
    const textInput = document.getElementById('textInput');
    const text = textInput.value.trim();
    
    if (!text) {
        alert('Please enter some text to process.');
        return;
    }
    
    if (isProcessing) return;
    
    showLoading(true);
    isProcessing = true;
    
    try {
        // Add as a document
        uploadedDocuments.push({
            name: 'Pasted Text',
            size: text.length,
            content: text,
            type: 'text/plain'
        });
        
        // Update document content
        documentContent = uploadedDocuments.map(doc => doc.content).join('\n\n');
        
        // Show chat interface
        showChatInterface();
        updateDocumentCount();
        
        // Add welcome message
        addMessage('bot', 'I\'ve processed your text content. You can now ask me questions about it!');
        
        // Clear the text input
        textInput.value = '';
        
    } catch (error) {
        console.error('Error processing text:', error);
        alert('Error processing text. Please try again.');
    } finally {
        showLoading(false);
        isProcessing = false;
    }
}

// Show chat interface
function showChatInterface() {
    const chatSection = document.getElementById('chatSection');
    if (chatSection) {
        chatSection.style.display = 'block';
    }
}

// Update document count
function updateDocumentCount() {
    const count = uploadedDocuments.length;
    document.getElementById('documentCount').textContent = `${count} document${count !== 1 ? 's' : ''} loaded`;
}

// Clear all documents
function clearDocuments() {
    uploadedDocuments = [];
    documentContent = '';
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.innerHTML = '';
    }
    const chatSection = document.getElementById('chatSection');
    if (chatSection) {
        chatSection.style.display = 'none';
    }
}

// Chat functionality
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage('user', message);
    
    // Clear input
    chatInput.value = '';
    
    // Process the question
    processQuestion(message);
}

function askQuestion(question) {
    document.getElementById('chatInput').value = question;
    sendMessage();
}

// Add message to chat
function addMessage(sender, content) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const icon = sender === 'bot' ? 'fas fa-robot' : 'fas fa-user';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <i class="${icon}"></i>
            <p>${content}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Process user questions
async function processQuestion(question) {
    if (!documentContent) {
        addMessage('bot', 'No documents are loaded. Please upload or paste some content first.');
        return;
    }
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        // Simulate AI processing (in a real app, this would call an AI API)
        const response = await generateAIResponse(question, documentContent);
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add bot response
        addMessage('bot', response);
        
    } catch (error) {
        console.error('Error processing question:', error);
        removeTypingIndicator(typingId);
        addMessage('bot', 'Sorry, I encountered an error processing your question. Please try again.');
    }
}

// Add typing indicator
function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-content">
            <i class="fas fa-robot"></i>
            <p><i class="fas fa-spinner fa-spin"></i> Thinking...</p>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return 'typing-indicator';
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Generate AI response (simulated)
async function generateAIResponse(question, content) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    const lowerQuestion = question.toLowerCase();
    
    // Simple keyword-based responses (in a real app, this would use AI/ML)
    if (lowerQuestion.includes('summarize') || lowerQuestion.includes('summary')) {
        return generateSummary(content);
    } else if (lowerQuestion.includes('key findings') || lowerQuestion.includes('main findings')) {
        return generateKeyFindings(content);
    } else if (lowerQuestion.includes('topics') || lowerQuestion.includes('main topics')) {
        return generateMainTopics(content);
    } else if (lowerQuestion.includes('what') || lowerQuestion.includes('how') || lowerQuestion.includes('why')) {
        return generateAnswer(question, content);
    } else {
        return generateGeneralResponse(question, content);
    }
}

// Generate summary
function generateSummary(content) {
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 10);
    const summaryLength = Math.min(5, Math.ceil(sentences.length / 3));
    const summary = sentences.slice(0, summaryLength).join('. ').trim();
    
    return `**Summary:**\n\n${summary}${summary.endsWith('.') ? '' : '.'}\n\nThis summary covers the main points from your document(s). Would you like me to elaborate on any specific aspect?`;
}

// Generate key findings
function generateKeyFindings(content) {
    const lines = content.split('\n').filter(line => line.trim().length > 20);
    const findings = lines.slice(0, 5).map((line, index) => `${index + 1}. ${line.trim()}`);
    
    return `**Key Findings:**\n\n${findings.join('\n')}\n\nThese are the main points I identified in your document(s). Let me know if you'd like more details about any of these findings.`;
}

// Generate main topics
function generateMainTopics(content) {
    const words = content.toLowerCase().split(/\s+/);
    const wordCount = {};
    
    // Count word frequency (excluding common words)
    const stopWords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'];
    
    words.forEach(word => {
        if (word.length > 3 && !stopWords.includes(word)) {
            wordCount[word] = (wordCount[word] || 0) + 1;
        }
    });
    
    const topics = Object.entries(wordCount)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 8)
        .map(([word, count]) => `• ${word} (${count} mentions)`);
    
    return `**Main Topics Discussed:**\n\n${topics.join('\n')}\n\nThese are the most frequently mentioned topics in your document(s). Would you like me to explain any of these topics in more detail?`;
}

// Generate answer to specific question
function generateAnswer(question, content) {
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 10);
    const relevantSentences = sentences.filter(sentence => 
        question.toLowerCase().split(' ').some(word => 
            word.length > 3 && sentence.toLowerCase().includes(word)
        )
    );
    
    if (relevantSentences.length > 0) {
        const answer = relevantSentences.slice(0, 3).join('. ').trim();
        return `Based on your document(s), here's what I found:\n\n${answer}${answer.endsWith('.') ? '' : '.'}\n\nThis information is directly related to your question. Would you like me to provide more details or clarify anything?`;
    } else {
        return `I couldn't find specific information related to "${question}" in your document(s). The content might not contain information about this topic, or you might want to try rephrasing your question. Could you ask about something else or provide more context?`;
    }
}

// Generate general response
function generateGeneralResponse(question, content) {
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 10);
    const randomSentences = sentences.slice(0, 2);
    
    return `I understand you're asking about "${question}". Based on your document(s), here's some relevant information:\n\n${randomSentences.join('. ')}${randomSentences.join('. ').endsWith('.') ? '' : '.'}\n\nIs there something specific you'd like to know more about? I can help you find more detailed information or answer other questions about your content.`;
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// ==================== CALCULATOR FUNCTIONALITY ====================

let calculatorDisplay = '';
let calculatorResult = 0;
let calculatorOperation = '';
let calculatorWaitingForOperand = false;

function initializeCalculator() {
    updateCalculatorDisplay();
}

function updateCalculatorDisplay() {
    const display = document.getElementById('calcDisplay');
    display.value = calculatorDisplay || '0';
}

function clearCalculator() {
    calculatorDisplay = '';
    calculatorResult = 0;
    calculatorOperation = '';
    calculatorWaitingForOperand = false;
    updateCalculatorDisplay();
}

function deleteLast() {
    calculatorDisplay = calculatorDisplay.slice(0, -1);
    updateCalculatorDisplay();
}

function appendToDisplay(value) {
    if (calculatorWaitingForOperand) {
        calculatorDisplay = '';
        calculatorWaitingForOperand = false;
    }
    
    if (value === '.' && calculatorDisplay.includes('.')) {
        return; // Prevent multiple decimal points
    }
    
    calculatorDisplay += value;
    updateCalculatorDisplay();
}

function calculateResult() {
    try {
        if (calculatorDisplay === '') return;
        
        // Replace × with * for evaluation
        const expression = calculatorDisplay.replace(/×/g, '*');
        const result = Function('"use strict"; return (' + expression + ')')();
        
        if (isNaN(result) || !isFinite(result)) {
            calculatorDisplay = 'Error';
        } else {
            calculatorDisplay = result.toString();
        }
        
        calculatorWaitingForOperand = true;
        updateCalculatorDisplay();
    } catch (error) {
        calculatorDisplay = 'Error';
        updateCalculatorDisplay();
    }
}

// ==================== CALENDAR FUNCTIONALITY ====================

let currentCalendarDate = new Date();

function initializeCalendar() {
    updateDigitalClock();
    generateCalendar();
    
    // Update clock every second
    setInterval(updateDigitalClock, 1000);
}

function initializeUTCTime() {
    updateUTCTime();
    
    // Update UTC time every second
    setInterval(updateUTCTime, 1000);
}

function updateUTCTime() {
    const now = new Date();
    const utcTimeElement = document.getElementById('utcTime');
    const utcDateElement = document.getElementById('utcDate');
    
    if (utcTimeElement) {
        const utcTimeString = now.toLocaleTimeString('en-US', { 
            timeZone: 'UTC',
            hour12: true,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        utcTimeElement.textContent = utcTimeString;
    }
    
    if (utcDateElement) {
        const utcDateString = now.toLocaleDateString('en-US', { 
            timeZone: 'UTC',
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        utcDateElement.textContent = utcDateString;
    }
}

function updateDigitalClock() {
    const now = new Date();
    const timeElement = document.getElementById('currentTime');
    const dateElement = document.getElementById('currentDate');
    
    if (timeElement) {
        const timeString = now.toLocaleTimeString('en-US', { 
            hour12: true,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        timeElement.textContent = timeString;
    }
    
    if (dateElement) {
        const dateString = now.toLocaleDateString('en-US', { 
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        dateElement.textContent = dateString;
    }
}

function generateCalendar() {
    const calendarElement = document.getElementById('calendar');
    if (!calendarElement) return;
    
    const year = currentCalendarDate.getFullYear();
    const month = currentCalendarDate.getMonth();
    const today = new Date();
    
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();
    
    let calendarHTML = `
        <div class="calendar-header">
            <button class="calendar-nav" onclick="previousMonth()">‹</button>
            <div class="calendar-title">${monthNames[month]} ${year}</div>
            <button class="calendar-nav" onclick="nextMonth()">›</button>
        </div>
        <div class="calendar-grid">
            <div class="calendar-day-header">Sun</div>
            <div class="calendar-day-header">Mon</div>
            <div class="calendar-day-header">Tue</div>
            <div class="calendar-day-header">Wed</div>
            <div class="calendar-day-header">Thu</div>
            <div class="calendar-day-header">Fri</div>
            <div class="calendar-day-header">Sat</div>
    `;
    
    // Add empty cells for days before the first day of the month
    for (let i = 0; i < startingDayOfWeek; i++) {
        const prevMonth = new Date(year, month, 0);
        const day = prevMonth.getDate() - startingDayOfWeek + i + 1;
        calendarHTML += `<div class="calendar-day other-month">${day}</div>`;
    }
    
    // Add days of the current month
    for (let day = 1; day <= daysInMonth; day++) {
        const isToday = year === today.getFullYear() && 
                       month === today.getMonth() && 
                       day === today.getDate();
        
        const dayClass = isToday ? 'calendar-day today' : 'calendar-day';
        calendarHTML += `<div class="${dayClass}" onclick="selectDate(${day})">${day}</div>`;
    }
    
    // Add empty cells for days after the last day of the month
    const remainingCells = 42 - (startingDayOfWeek + daysInMonth);
    for (let day = 1; day <= remainingCells; day++) {
        calendarHTML += `<div class="calendar-day other-month">${day}</div>`;
    }
    
    calendarHTML += '</div>';
    calendarElement.innerHTML = calendarHTML;
}

function previousMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
    generateCalendar();
}

function nextMonth() {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
    generateCalendar();
}

function selectDate(day) {
    // You can add functionality here for when a date is selected
    console.log(`Selected date: ${currentCalendarDate.getFullYear()}-${currentCalendarDate.getMonth() + 1}-${day}`);
}

// ==================== UTC TIME FUNCTIONALITY ====================
// (Currency converter functionality removed and replaced with UTC time)

// ==================== TIME ZONE MAP FUNCTIONALITY ====================

let globeRotation = {
    x: -15,
    y: 0
};

let isDragging = false;
let previousMousePosition = {
    x: 0,
    y: 0
};

let earthCanvas, earthCtx;
let earthRadius = 70;
let earthCenterX, earthCenterY;

function initializeTimezoneMap() {
    updateTimezoneTime();
    // Update timezone time every second
    setInterval(updateTimezoneTime, 1000);
    
    // Initialize 3D Earth globe
    initialize3DEarth();
}

function initialize3DEarth() {
    const canvas = document.getElementById('earthCanvas');
    if (!canvas) return;
    
    earthCanvas = canvas;
    earthCtx = canvas.getContext('2d');
    earthCenterX = canvas.width / 2;
    earthCenterY = canvas.height / 2;
    
    // Create Earth texture pattern
    createEarthTexture();
    
    // Set up interaction
    setupGlobeInteraction();
    
    // Start animation
    animateEarth();
}

function createEarthTexture() {
    // This function creates a canvas-based Earth texture
    // We'll draw continents and oceans on a separate canvas
    const textureCanvas = document.createElement('canvas');
    textureCanvas.width = 360;
    textureCanvas.height = 180;
    const texCtx = textureCanvas.getContext('2d');
    
    // Draw ocean base
    texCtx.fillStyle = '#1e40af';
    texCtx.fillRect(0, 0, textureCanvas.width, textureCanvas.height);
    
    // Draw darker ocean areas
    const oceanGradient = texCtx.createLinearGradient(0, 0, 0, textureCanvas.height);
    oceanGradient.addColorStop(0, '#0a4d8c');
    oceanGradient.addColorStop(0.5, '#0a3a6b');
    oceanGradient.addColorStop(1, '#0a2a4f');
    texCtx.fillStyle = oceanGradient;
    texCtx.fillRect(0, 0, textureCanvas.width, textureCanvas.height);
    
    // Draw continents (simplified shapes)
    // North America
    texCtx.fillStyle = '#2d5016';
    texCtx.beginPath();
    texCtx.ellipse(80, 50, 45, 35, 0, 0, 2 * Math.PI);
    texCtx.fill();
    
    // South America
    texCtx.beginPath();
    texCtx.ellipse(100, 120, 25, 50, 0.3, 0, 2 * Math.PI);
    texCtx.fill();
    
    // Europe/Africa
    texCtx.fillStyle = '#3d6b1f';
    texCtx.beginPath();
    texCtx.ellipse(170, 70, 30, 80, 0, 0, 2 * Math.PI);
    texCtx.fill();
    
    // Asia
    texCtx.fillStyle = '#4a7c28';
    texCtx.beginPath();
    texCtx.ellipse(240, 50, 50, 40, 0, 0, 2 * Math.PI);
    texCtx.fill();
    
    // Australia
    texCtx.fillStyle = '#2d5016';
    texCtx.beginPath();
    texCtx.ellipse(280, 130, 25, 20, 0, 0, 2 * Math.PI);
    texCtx.fill();
    
    // Add desert regions
    texCtx.fillStyle = '#8b7355';
    texCtx.beginPath();
    texCtx.ellipse(170, 100, 40, 30, 0, 0, 2 * Math.PI);
    texCtx.fill();
    
    // Polar ice caps
    const iceGradient = texCtx.createRadialGradient(180, 0, 0, 180, 0, 40);
    iceGradient.addColorStop(0, 'rgba(255, 255, 255, 0.9)');
    iceGradient.addColorStop(1, 'rgba(200, 220, 240, 0.5)');
    texCtx.fillStyle = iceGradient;
    texCtx.beginPath();
    texCtx.ellipse(180, 10, 180, 25, 0, 0, 2 * Math.PI);
    texCtx.fill();
    
    texCtx.beginPath();
    texCtx.ellipse(180, 170, 180, 25, 0, 0, 2 * Math.PI);
    texCtx.fill();
    
    // Store texture
    earthCanvas.earthTexture = textureCanvas;
}

function draw3DEarth() {
    const ctx = earthCtx;
    const canvas = earthCanvas;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const texture = canvas.earthTexture;
    if (!texture) return;
    
    const radius = earthRadius;
    const centerX = earthCenterX;
    const centerY = earthCenterY;
    
    // Calculate rotation
    const rotY = globeRotation.y * Math.PI / 180;
    const rotX = globeRotation.x * Math.PI / 180;
    
    // Draw sphere with 3D projection
    const imageData = ctx.createImageData(canvas.width, canvas.height);
    const data = imageData.data;
    
    for (let y = 0; y < canvas.height; y++) {
        for (let x = 0; x < canvas.width; x++) {
            const dx = x - centerX;
            const dy = y - centerY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist <= radius) {
                // Calculate 3D position
                const z = Math.sqrt(radius * radius - dist * dist);
                const nx = dx / radius;
                const ny = dy / radius;
                const nz = z / radius;
                
                // Apply rotations
                let px = nx;
                let py = ny;
                let pz = nz;
                
                // Rotate around Y axis
                const tempX = px * Math.cos(rotY) + pz * Math.sin(rotY);
                const tempZ = -px * Math.sin(rotY) + pz * Math.cos(rotY);
                px = tempX;
                pz = tempZ;
                
                // Rotate around X axis
                const tempY = py * Math.cos(rotX) - pz * Math.sin(rotX);
                pz = py * Math.sin(rotX) + pz * Math.cos(rotX);
                py = tempY;
                
                // Map to texture coordinates
                const u = (Math.atan2(px, pz) + Math.PI) / (2 * Math.PI);
                const v = (Math.asin(py) + Math.PI / 2) / Math.PI;
                
                const texX = Math.floor(u * texture.width) % texture.width;
                const texY = Math.floor(v * texture.height);
                
                // Get color from texture
                const texCtx = texture.getContext('2d');
                const texImageData = texCtx.getImageData(texX, texY, 1, 1);
                const r = texImageData.data[0];
                const g = texImageData.data[1];
                const b = texImageData.data[2];
                
                // Apply lighting (use rotated normal)
                const lightX = 0.5;
                const lightY = -0.5;
                const lightZ = 1;
                const lightLength = Math.sqrt(lightX * lightX + lightY * lightY + lightZ * lightZ);
                const dot = (px * lightX + py * lightY + pz * lightZ) / lightLength;
                const lightIntensity = Math.max(0, dot);
                const ambient = 0.3;
                const brightness = ambient + (1 - ambient) * lightIntensity;
                
                const index = (y * canvas.width + x) * 4;
                data[index] = Math.min(255, r * brightness);
                data[index + 1] = Math.min(255, g * brightness);
                data[index + 2] = Math.min(255, b * brightness);
                data[index + 3] = 255;
            }
        }
    }
    
    ctx.putImageData(imageData, 0, 0);
    
    // Draw atmospheric glow
    const gradient = ctx.createRadialGradient(centerX, centerY, radius * 0.9, centerX, centerY, radius * 1.2);
    gradient.addColorStop(0, 'transparent');
    gradient.addColorStop(1, 'rgba(100, 150, 255, 0.15)');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 1.15, 0, 2 * Math.PI);
    ctx.fill();
}

function animateEarth() {
    draw3DEarth();
    requestAnimationFrame(animateEarth);
}

function setupGlobeInteraction() {
    const globeContainer = document.getElementById('globeContainer');
    if (!globeContainer) return;
    
    globeContainer.addEventListener('mousedown', (e) => {
        isDragging = true;
        previousMousePosition.x = e.clientX;
        previousMousePosition.y = e.clientY;
        globeContainer.style.cursor = 'grabbing';
    });
    
    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        
        const deltaX = e.clientX - previousMousePosition.x;
        const deltaY = e.clientY - previousMousePosition.y;
        
        globeRotation.y += deltaX * 0.5;
        globeRotation.x += deltaY * 0.5;
        globeRotation.x = Math.max(-90, Math.min(90, globeRotation.x));
        
        previousMousePosition.x = e.clientX;
        previousMousePosition.y = e.clientY;
    });
    
    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            globeContainer.style.cursor = 'grab';
        }
    });
    
    globeContainer.addEventListener('touchstart', (e) => {
        e.preventDefault();
        isDragging = true;
        previousMousePosition.x = e.touches[0].clientX;
        previousMousePosition.y = e.touches[0].clientY;
    });
    
    document.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        
        const deltaX = e.touches[0].clientX - previousMousePosition.x;
        const deltaY = e.touches[0].clientY - previousMousePosition.y;
        
        globeRotation.y += deltaX * 0.5;
        globeRotation.x += deltaY * 0.5;
        globeRotation.x = Math.max(-90, Math.min(90, globeRotation.x));
        
        previousMousePosition.x = e.touches[0].clientX;
        previousMousePosition.y = e.touches[0].clientY;
    });
    
    document.addEventListener('touchend', () => {
        isDragging = false;
    });
}

function updateTimezoneTime() {
    const timezoneSelect = document.getElementById('timezoneSelect');
    const timezoneTimeElement = document.getElementById('timezoneTime');
    const timezoneDateElement = document.getElementById('timezoneDate');
    const timezoneNameElement = document.getElementById('timezoneName');
    
    if (!timezoneSelect || !timezoneTimeElement || !timezoneDateElement || !timezoneNameElement) {
        return;
    }
    
    const selectedTimezone = timezoneSelect.value;
    const now = new Date();
    
    try {
        // Format timezone name for display
        const timezoneParts = selectedTimezone.split('/');
        const displayName = timezoneParts[timezoneParts.length - 1].replace(/_/g, ' ');
        
        // Get time in selected timezone
        const timeString = now.toLocaleTimeString('en-US', {
            timeZone: selectedTimezone,
            hour12: true,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        const dateString = now.toLocaleDateString('en-US', {
            timeZone: selectedTimezone,
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        // Calculate UTC offset
        const utcTime = new Date(now.toLocaleString('en-US', { timeZone: 'UTC' }));
        const localTime = new Date(now.toLocaleString('en-US', { timeZone: selectedTimezone }));
        const offset = (localTime - utcTime) / (1000 * 60 * 60); // Offset in hours
        
        let offsetString = offset >= 0 ? '+' : '';
        offsetString += offset.toFixed(0);
        if (offset % 1 !== 0) {
            offsetString += ':' + (Math.abs(offset % 1) * 60).toFixed(0).padStart(2, '0');
        }
        
        timezoneTimeElement.textContent = timeString;
        timezoneDateElement.textContent = dateString;
        timezoneNameElement.textContent = `${displayName} (UTC${offsetString})`;
    } catch (error) {
        console.error('Error updating timezone time:', error);
        timezoneTimeElement.textContent = 'Error';
        timezoneDateElement.textContent = 'Unable to load timezone';
        timezoneNameElement.textContent = selectedTimezone;
    }
}

// ==================== PERCENTAGE CONVERTER ====================

function initializePercentageConverter() {
    // Initialize with default values
    calculatePercentage();
}

function calculatePercentage() {
    const valueInput = document.getElementById('valueInput');
    const percentageInput = document.getElementById('percentageInput');
    const resultElement = document.getElementById('percentageResult');
    const subtractResultElement = document.getElementById('percentageSubtractResult');
    const addResultElement = document.getElementById('percentageAddResult');
    const breakdownElement = document.getElementById('percentageBreakdown');
    
    if (!valueInput || !percentageInput || !resultElement || !subtractResultElement || !addResultElement || !breakdownElement) {
        return;
    }
    
    const value = parseFloat(valueInput.value);
    const percentage = parseFloat(percentageInput.value);
    
    // Clear result if inputs are invalid
    if (isNaN(value) || isNaN(percentage) || valueInput.value === '' || percentageInput.value === '') {
        resultElement.textContent = '0';
        subtractResultElement.textContent = '0';
        addResultElement.textContent = '0';
        breakdownElement.classList.add('hide');
        breakdownElement.innerHTML = '';
        return;
    }
    
    // Calculate the result
    const result = (value * percentage) / 100;
    const subtractResult = value - result;
    const addResult = value + result;
    
    // Format the result with proper decimals
    const formattedResult = formatNumber(result);
    const formattedSubtractResult = formatNumber(subtractResult);
    const formattedAddResult = formatNumber(addResult);
    const formattedValue = formatNumber(value);
    const formattedPercentage = formatNumber(percentage);
    
    // Display the results
    resultElement.textContent = formattedResult;
    subtractResultElement.textContent = formattedSubtractResult;
    addResultElement.textContent = formattedAddResult;
    
    // Show breakdown
    breakdownElement.classList.remove('hide');
    breakdownElement.innerHTML = `
        <div class="percentage-breakdown-item">
            <strong>Calculation:</strong> ${formattedValue} × ${formattedPercentage}% = ${formattedResult}
        </div>
        <div class="percentage-breakdown-item">
            <strong>Percentage Amount:</strong> ${formattedResult}
        </div>
        <div class="percentage-breakdown-item">
            <strong>Original Value:</strong> ${formattedValue}
        </div>
        <div class="percentage-breakdown-item">
            <strong>Value Minus Percentage:</strong> ${formattedSubtractResult}
        </div>
        <div class="percentage-breakdown-item">
            <strong>Value Plus Percentage:</strong> ${formattedAddResult}
        </div>
    `;
}

function formatNumber(num) {
    // Format number to show up to 2 decimal places, removing unnecessary zeros
    if (num % 1 === 0) {
        return num.toString();
    }
    return parseFloat(num.toFixed(2)).toString();
}

function clearPercentageCalculator() {
    const valueInput = document.getElementById('valueInput');
    const percentageInput = document.getElementById('percentageInput');
    const resultElement = document.getElementById('percentageResult');
    const subtractResultElement = document.getElementById('percentageSubtractResult');
    const addResultElement = document.getElementById('percentageAddResult');
    const breakdownElement = document.getElementById('percentageBreakdown');
    
    if (valueInput) valueInput.value = '';
    if (percentageInput) percentageInput.value = '';
    if (resultElement) resultElement.textContent = '0';
    if (subtractResultElement) subtractResultElement.textContent = '0';
    if (addResultElement) addResultElement.textContent = '0';
    if (breakdownElement) {
        breakdownElement.classList.add('hide');
        breakdownElement.innerHTML = '';
    }
}

// ==================== RANDOM JOKE GENERATOR ====================

const jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why did the math book look so sad? Because it had too many problems!",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
    "Why don't programmers like nature? It has too many bugs!",
    "How do you organize a space party? You planet!",
    "Why did the coffee file a police report? It got mugged!",
    "What do you call a fake noodle? An impasta!",
    "Why did the cookie go to the doctor? Because it felt crummy!",
    "What's a computer's favorite snack? Microchips!",
    "Why don't programmers like to go outside? The sun gives them compiler errors!",
    "What did one wall say to the other wall? I'll meet you at the corner!",
    "Why was the math book sad? Because it had too many problems!",
    "What do you call a sleeping bull? A bulldozer!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    "What do you call a bear with no socks on? Barefoot!",
    "Why don't scientists trust stairs? Because they're always up to something!",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "Why did the bicycle fall over? Because it was two tired!",
    "What's orange and sounds like a parrot? A carrot!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "What do you call a fish wearing a bowtie? Sofishticated!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "What's a computer's favorite beat? An algorithm!",
    "Why did the coffee file a police report? It got mugged!",
    "What do you call a factory that makes okay products? A satisfactory!",
    "Why did the math teacher break up with the geography teacher? Because they had irreconcilable differences!",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Why don't programmers like to go outside? There are too many bugs in the world!",
    "What's a skeleton's favorite instrument? The trombone!",
    "Why did the scarecrow get promoted? He was outstanding in his field!",
    "What do you call a bear with no teeth? A gummy bear!"
];

function initializeJokeGenerator() {
    // Generate a joke on page load
    generateRandomJoke();
}

function generateRandomJoke() {
    const jokeTextElement = document.getElementById('jokeText');
    
    if (!jokeTextElement) {
        return;
    }
    
    // Get a random joke
    const randomIndex = Math.floor(Math.random() * jokes.length);
    const randomJoke = jokes[randomIndex];
    
    // Add fade effect
    jokeTextElement.style.opacity = '0';
    
    setTimeout(() => {
        jokeTextElement.textContent = randomJoke;
        
        jokeTextElement.style.transition = 'opacity 0.3s ease';
        jokeTextElement.style.opacity = '1';
    }, 150);
}

// ==================== INITIALIZATION ====================

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize widgets
    initializeCalculator();
    initializeCalendar();
    initializeUTCTime();
    initializeTimezoneMap();
    initializePercentageConverter();
    initializeJokeGenerator();
});
