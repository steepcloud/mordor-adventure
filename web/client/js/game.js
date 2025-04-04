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
            
            // Display initial messages
            appendToOutput(data.messages.join('\n'));
            
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
                
                // Check if game is over
                if (data.game_over) {
                    appendToOutput('\n\nGame Over! Refresh the page to start a new game.');
                    commandInput.disabled = true;
                }
                
            } catch (error) {
                console.error('Error processing command:', error);
                appendToOutput('\nError connecting to game server. Please try again.');
            }
        }
    });
    
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
                element.textContent = baseText + text.substring(0, i + 1);
                i++;
                element.parentElement.scrollTop = element.parentElement.scrollHeight;
                
                // Random speed variation for more realistic typing
                const randomSpeed = speed + Math.random() * 10;
                setTimeout(type, randomSpeed);
            }
        }
        
        type();
    }
    
    // CRT Effect on startup - turn on animation
    setTimeout(() => {
        document.body.classList.add('crt-on');
    }, 500);
});