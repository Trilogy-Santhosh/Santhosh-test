// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Update last updated time
    document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
    
    // Counter functionality
    let count = 0;
    const countDisplay = document.getElementById('count');
    const increaseBtn = document.getElementById('increase');
    const decreaseBtn = document.getElementById('decrease');
    const resetBtn = document.getElementById('reset');
    
    function updateCount() {
        countDisplay.textContent = count;
        countDisplay.style.color = count > 0 ? '#48bb78' : count < 0 ? '#f56565' : '#667eea';
    }
    
    increaseBtn.addEventListener('click', function() {
        count++;
        updateCount();
        animateButton(this);
    });
    
    decreaseBtn.addEventListener('click', function() {
        count--;
        updateCount();
        animateButton(this);
    });
    
    resetBtn.addEventListener('click', function() {
        count = 0;
        updateCount();
        animateButton(this);
    });
    
    // Color changer functionality
    const colorBox = document.getElementById('colorBox');
    const redBtn = document.getElementById('red');
    const blueBtn = document.getElementById('blue');
    const greenBtn = document.getElementById('green');
    const randomBtn = document.getElementById('random');
    
    function changeColor(color) {
        colorBox.style.backgroundColor = color;
        colorBox.style.transform = 'scale(1.1)';
        setTimeout(() => {
            colorBox.style.transform = 'scale(1)';
        }, 200);
    }
    
    redBtn.addEventListener('click', function() {
        changeColor('#e53e3e');
        animateButton(this);
    });
    
    blueBtn.addEventListener('click', function() {
        changeColor('#3182ce');
        animateButton(this);
    });
    
    greenBtn.addEventListener('click', function() {
        changeColor('#38a169');
        animateButton(this);
    });
    
    randomBtn.addEventListener('click', function() {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd'];
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        changeColor(randomColor);
        animateButton(this);
    });
    
    // Todo list functionality
    const todoInput = document.getElementById('todoInput');
    const addTodoBtn = document.getElementById('addTodo');
    const todoList = document.getElementById('todoList');
    let todoId = 0;
    
    function addTodo() {
        const text = todoInput.value.trim();
        if (text === '') {
            alert('Please enter a task!');
            return;
        }
        
        const todoItem = document.createElement('li');
        todoItem.className = 'todo-item';
        todoItem.dataset.id = todoId++;
        
        todoItem.innerHTML = `
            <span>${text}</span>
            <div>
                <button onclick="toggleTodo(${todoItem.dataset.id})">Toggle</button>
                <button onclick="deleteTodo(${todoItem.dataset.id})">Delete</button>
            </div>
        `;
        
        todoList.appendChild(todoItem);
        todoInput.value = '';
        
        // Add animation
        todoItem.style.opacity = '0';
        todoItem.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            todoItem.style.transition = 'all 0.3s ease';
            todoItem.style.opacity = '1';
            todoItem.style.transform = 'translateX(0)';
        }, 10);
    }
    
    addTodoBtn.addEventListener('click', addTodo);
    
    todoInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo();
        }
    });
    
    // Global functions for todo actions
    window.toggleTodo = function(id) {
        const todoItem = document.querySelector(`[data-id="${id}"]`);
        if (todoItem) {
            todoItem.classList.toggle('completed');
        }
    };
    
    window.deleteTodo = function(id) {
        const todoItem = document.querySelector(`[data-id="${id}"]`);
        if (todoItem) {
            todoItem.style.transition = 'all 0.3s ease';
            todoItem.style.opacity = '0';
            todoItem.style.transform = 'translateX(20px)';
            setTimeout(() => {
                todoItem.remove();
            }, 300);
        }
    };
    
    // Button animation function
    function animateButton(button) {
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 150);
    }
    
    // Add some fun interactions
    document.addEventListener('keydown', function(e) {
        // Keyboard shortcuts
        switch(e.key) {
            case '+':
            case '=':
                if (e.ctrlKey) {
                    e.preventDefault();
                    increaseBtn.click();
                }
                break;
            case '-':
                if (e.ctrlKey) {
                    e.preventDefault();
                    decreaseBtn.click();
                }
                break;
            case 'r':
                if (e.ctrlKey) {
                    e.preventDefault();
                    resetBtn.click();
                }
                break;
        }
    });
    
    // Add some console fun
    console.log('🚀 Welcome to Santhosh\'s Test App!');
    console.log('💡 Try these keyboard shortcuts:');
    console.log('   Ctrl + + : Increase counter');
    console.log('   Ctrl + - : Decrease counter');
    console.log('   Ctrl + R : Reset counter');
    console.log('🎨 Enjoy the interactive features!');
});
