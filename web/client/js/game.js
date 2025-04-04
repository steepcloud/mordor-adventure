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
            
            // update player info
            playerNameDisplay.textContent = data.player.name;
            updateHealthDisplay(data.player.health, data.player.max_health);
            
            // switch to game screen
            startupScreen.style.display = 'none';
            gameScreen.style.display = 'flex';
            
            // focus on command input
            commandInput.focus();
            
            // adding typewriter effect to initial text
            typewriterEffect(output, data.messages.join('\n'), 0, 10);
            
        } catch (error) {
            console.error('Error starting game:', error);
            appendToOutput('Error connecting to game server. Please try again.');
        }
    });
    
    commandInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const command = commandInput.value.trim();
            if (!command) return;
            
            // clear input
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
                
                // update player info
                playerNameDisplay.textContent = data.player.name;
                updateHealthDisplay(data.player.health, data.player.max_health);
                
                // display new messages with typewriter effect
                typewriterEffect(output, '\n' + data.messages.join('\n'), output.textContent.length, 10);
                
                // scroll to bottom
                output.parentElement.scrollTop = output.parentElement.scrollHeight;
                
                if (checkForGameOver(data)) {
                    return;
                }
                else if (data.quit) {
                    console.log("Quit condition detected!");
                    showQuitScreen();
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

    function showQuitScreen() {
        console.log("Showing quit screen");

        let container = document.querySelector('.terminal-content');
        if (!container) {
            container = output.parentElement;
        }

        if (container) {
            container.innerHTML = '';
        } else {
            output.innerHTML = '';
        }

        const quitMessage = document.createElement('div');
        quitMessage.className = 'quit-message';
        quitMessage.innerHTML = `
            <h2>Thank you for playing!</h2>
            <p>You have quit the game.</p>
            <button id="return-to-menu">Return to Main Menu</button>
        `;

        if (container) {
            container.appendChild(quitMessage);
        } else {
            output.appendChild(quitMessage);
        }

        document.getElementById('return-to-menu').addEventListener('click', () => {
            document.querySelector('#game-screen').style.display = 'none';
            document.querySelector('#startup-screen').style.display = 'block';
        });

        commandInput.disabled = true;
    }

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
        
        // change color based on health percentage
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
                
                // random speed variation for more realistic typing
                const randomSpeed = speed + Math.random() * 10;
                setTimeout(type, randomSpeed);
            }
        }
        
        type();
    }

    function showGameOverScreen() {
        console.log("Showing game over screen!");
        
        // finding the correct container - using fallbacks if needed
        let container = document.querySelector('.terminal-content');
        if (!container) {
            container = output.parentElement;
        }
        
        // clear the content
        if (container) {
            container.innerHTML = '';
        } else {
            // if no container found, just clear the output
            output.innerHTML = '';
        }
        
        // create the game over elements
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

        gameOverContainer.appendChild(gameOverText);
        gameOverContainer.appendChild(retryText);

        if (container) {
            container.appendChild(gameOverContainer);
        } else {
            output.innerHTML = '';
            output.appendChild(gameOverContainer);
        }
        
        gameOverContainer.style.display = 'block';

        commandInput.disabled = true;

        if (document.getElementById('enemy-info')) {
            document.getElementById('enemy-info').style.display = 'none';
        }
    }
    
    // CRT effect on startup - turn on animation
    setTimeout(() => {
        document.body.classList.add('crt-on');
    }, 500);
});