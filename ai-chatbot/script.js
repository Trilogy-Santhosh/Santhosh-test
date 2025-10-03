// Global variables
let uploadedDocuments = [];
let documentContent = '';
let isProcessing = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up file input event listener
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', handleFileUpload);
    
    // Set up drag and drop
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    
    // Set up chat input
    const chatInput = document.getElementById('chatInput');
    chatInput.addEventListener('keypress', handleKeyPress);
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
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('chatSection').style.display = 'block';
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
    document.getElementById('chatMessages').innerHTML = '';
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('chatSection').style.display = 'none';
    document.getElementById('fileInput').value = '';
    document.getElementById('textInput').value = '';
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

function updateDigitalClock() {
    const now = new Date();
    const timeElement = document.getElementById('currentTime');
    const dateElement = document.getElementById('currentDate');
    
    if (timeElement) {
        const timeString = now.toLocaleTimeString('en-US', { 
            hour12: false,
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

// ==================== CURRENCY CONVERTER FUNCTIONALITY ====================

let currentExchangeRate = 88.79; // Current rate as of today

async function initializeCurrencyConverter() {
    // Set initial exchange rate display with fallback
    document.getElementById('exchangeRate').textContent = `1 USD = ${currentExchangeRate} INR`;
    // Convert with the default USD value of 1
    convertCurrency();
    
    // Try to fetch real-time rate
    await updateExchangeRate();
}

function convertCurrency() {
    const usdAmount = parseFloat(document.getElementById('usdAmount').value) || 0;
    const inrAmount = usdAmount * currentExchangeRate;
    
    document.getElementById('inrAmount').value = inrAmount.toFixed(2);
}

async function updateExchangeRate() {
    const exchangeRateElement = document.getElementById('exchangeRate');
    const refreshButton = document.querySelector('.refresh-rate');
    
    // Show loading state
    if (refreshButton) {
        refreshButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        refreshButton.disabled = true;
    }
    
    try {
        // Fetch real-time exchange rate from a free API
        const response = await fetch('https://api.exchangerate-api.com/v4/latest/USD');
        const data = await response.json();
        
        if (data && data.rates && data.rates.INR) {
            currentExchangeRate = data.rates.INR;
            exchangeRateElement.textContent = `1 USD = ${currentExchangeRate.toFixed(2)} INR`;
            convertCurrency();
        } else {
            // Fallback to current known rate if API fails
            currentExchangeRate = 88.79;
            exchangeRateElement.textContent = `1 USD = ${currentExchangeRate} INR`;
            convertCurrency();
        }
    } catch (error) {
        console.log('Exchange rate API unavailable, using fallback rate');
        // Fallback to current known rate if API fails
        currentExchangeRate = 88.79;
        exchangeRateElement.textContent = `1 USD = ${currentExchangeRate} INR`;
        convertCurrency();
    } finally {
        // Reset button state
        if (refreshButton) {
            refreshButton.innerHTML = '<i class="fas fa-sync-alt"></i>';
            refreshButton.disabled = false;
        }
    }
}

// ==================== INITIALIZATION ====================

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    
    // File input change event
    fileInput.addEventListener('change', handleFileUpload);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Initialize widgets
    initializeCalculator();
    initializeCalendar();
    initializeCurrencyConverter();
});
