document.addEventListener('DOMContentLoaded', () => {
    let gameId = null;
    const output = document.getElementById('output');
    const commandInput = document.getElementById('command-input');
    const playerNameDisplay = document.getElementById('player-name');
    const playerHealthDisplay = document.getElementById('player-health');
    const gameScreen = document.getElementById('game-screen');
    const startupScreen = document.getElementById('startup-screen');
    const startButton = document.getElementById('start-button');
    const playerNameInput = document.getElementById('player-name-input');
    const raceSelect = document.getElementById('race-select');

    startButton.addEventListener('click', async () => {
        const playerName = playerNameInput.value.trim() || 'Adventurer';
        const race = raceSelect.value;
        
        try {
            const response = await fetch('http://localhost:5000/api/new_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: playerName,
                    race: race
                })
            });
            
            const data = await response.json();
            gameId = data.game_id;
            
            // Update player info
            playerNameDisplay.textContent = data.player.name;
            updateHealthDisplay(data.player.health, data.player.max_health);
            
            // Switch to game screen
            startupScreen.style.display = 'none';
            gameScreen.style.display = 'flex';
            
            // Focus on command input
            commandInput.focus();
            
            // Add typewriter effect to initial text
            typewriterEffect(output, data.messages.join('\n'), 0, 10);
            
        } catch (error) {
            console.error('Error starting game:', error);
            appendToOutput('Error connecting to game server. Please try again.');
        }
    });
    
    // Command input event
    commandInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            console.log("Current output content:", output.textContent);
            console.log("Output contains welcome msg:", 
                   output.textContent.includes("Welcome to the Lands of Mordor"));
        
            e.preventDefault();
            const command = commandInput.value.trim();
            if (!command) return;
            
            // Clear input
            commandInput.value = '';
            
            try {
                const response = await fetch('http://localhost:5000/api/command', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        game_id: gameId,
                        command: command
                    })
                });
                
                const data = await response.json();
                
                // Update player info
                playerNameDisplay.textContent = data.player.name;
                updateHealthDisplay(data.player.health, data.player.max_health);
                
                // Display new messages with typewriter effect
                typewriterEffect(output, '\n' + data.messages.join('\n'), output.textContent.length, 10);
                
                // Scroll to bottom
                output.parentElement.scrollTop = output.parentElement.scrollHeight;
                
                if (checkForGameOver(data)) {
                    return;
                }
                
                if (data.in_combat) {
                    setTimeout(() => {
                        if (data.player.health <= 0) {
                            console.log("Delayed death detection!");
                            showGameOverScreen();
                            commandInput.disabled = true;
                        }
                    }, 2000);
                }
                
            } catch (error) {
                console.error('Error processing command:', error);
                appendToOutput('\nError connecting to game server. Please try again.');
            }
        }
    });

    function checkForGameOver(data) {
        console.log("Checking game over status:", data.player.health, data.game_over);
        if (data.player.health <= 0 || data.game_over) {
            console.log("Game over condition detected!");
            showGameOverScreen();
            commandInput.disabled = true;
            return true;
        }
        return false;
    }
    
    // Helper functions
    function appendToOutput(text) {
        output.textContent += text;
        output.parentElement.scrollTop = output.parentElement.scrollHeight;
    }
    
    function updateHealthDisplay(health, maxHealth) {
        playerHealthDisplay.textContent = `HP: ${health}/${maxHealth}`;
        
        // Change color based on health percentage
        const healthPercent = (health / maxHealth) * 100;
        if (healthPercent < 25) {
            playerHealthDisplay.style.color = '#ff4444';
        } else if (healthPercent < 50) {
            playerHealthDisplay.style.color = '#ffaa44';
        } else {
            playerHealthDisplay.style.color = '#44ff44';
        }
    }
    
    function typewriterEffect(element, text, startPos, speed) {
        const baseText = element.textContent;
        let i = 0;
        
        function type() {
            if (i < text.length) {
                if (!element || !document.body.contains(element)) {
                    console.log("Element no longer in document, stopping typewriter effect");
                    return;
                }
                element.textContent = baseText + text.substring(0, i + 1);
                i++;

                if (element.parentElement) {
                    element.parentElement.scrollTop = element.parentElement.scrollHeight;
                }
                
                // Random speed variation for more realistic typing
                const randomSpeed = speed + Math.random() * 10;
                setTimeout(type, randomSpeed);
            }
        }
        
        type();
    }

    function showGameOverScreen() {
        console.log("Showing game over screen!");
        
        // Find the correct container - using fallbacks if needed
        let container = document.querySelector('.terminal-content');
        if (!container) {
            container = output.parentElement;
        }
        
        // Clear the content
        if (container) {
            container.innerHTML = '';
        } else {
            // If no container found, just clear the output
            output.innerHTML = '';
        }
        
        // Create the game over elements
        const gameOverContainer = document.createElement('div');
        gameOverContainer.className = 'game-over-container';
        
        const gameOverText = document.createElement('pre');
        gameOverText.className = 'game-over flashing';
        gameOverText.innerHTML = `
    ▄████  ▄▄▄       ███▄ ▄███▓▓█████     ▒█████   ██▒   █▓▓█████  ██▀███  
    ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒
    ▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███      ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒
    ░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  
    ░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒
    ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░
    ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░
    ░ ░   ░   ░   ▒   ░      ░      ░      ░ ░ ░ ▒       ░░     ░     ░░   ░ 
        ░       ░  ░       ░      ░  ░       ░ ░        ░     ░  ░   ░     
                                                        ░                    
    `;
        
        const retryText = document.createElement('div');
        retryText.className = 'retry-text';
        retryText.textContent = 'Press F5 to try again';
        
        // Append elements
        gameOverContainer.appendChild(gameOverText);
        gameOverContainer.appendChild(retryText);
        
        // Append to the right container
        if (container) {
            container.appendChild(gameOverContainer);
        } else {
            // Last resort - replace output content
            output.innerHTML = '';
            output.appendChild(gameOverContainer);
        }
        
        // Ensure the game over screen is visible
        gameOverContainer.style.display = 'block';
        
        // Disable input
        commandInput.disabled = true;
        
        // Hide any combat UI elements
        if (document.getElementById('enemy-info')) {
            document.getElementById('enemy-info').style.display = 'none';
        }
    }
    
    // CRT Effect on startup - turn on animation
    setTimeout(() => {
        document.body.classList.add('crt-on');
    }, 500);
});