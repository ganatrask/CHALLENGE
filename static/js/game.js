// Game state
let gameState = {
    sessionId: null,
    agentProfiles: [],
    currentPhase: 'setup',
    currentTopic: null,
    selectedPolicies: {},
    budgetUsed: 0,
    budgetRemaining: 14,
    discussionHistory: []
};

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    // DOM elements
    const startGameBtn = document.getElementById('start-game-btn');
    const introScreen = document.getElementById('intro-screen');
    const gameScreen = document.getElementById('game-screen');
    const policyAreasContainer = document.getElementById('policy-areas-container');
    const completeIndividualPhaseBtn = document.getElementById('complete-individual-phase');
    const individualPhase = document.getElementById('individual-phase');
    const groupPhase = document.getElementById('group-phase');
    const reflectionPhase = document.getElementById('reflection-phase');
    const agentsContainer = document.getElementById('agents-container');
    const budgetUsedEl = document.getElementById('budget-used');
    const budgetDisplayEl = document.getElementById('budget-display');
    const budgetFeedbackEl = document.getElementById('budget-feedback');
    const currentTopicEl = document.getElementById('current-topic');
    const discussionLogEl = document.getElementById('discussion-log');
    const humanArgument = document.getElementById('human-argument');
    const humanStance = document.getElementById('human-stance');
    const submitArgumentBtn = document.getElementById('submit-argument-btn');
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const finalizeOptionBtns = document.querySelectorAll('.finalize-option');
    const policySummaryTable = document.getElementById('policy-summary-table');
    const totalBudgetUsedEl = document.getElementById('total-budget-used');
    const equityScoreEl = document.getElementById('equity-score');
    const equityAnalysisEl = document.getElementById('equity-analysis');
    const justiceScoreEl = document.getElementById('justice-score');
    const justiceAnalysisEl = document.getElementById('justice-analysis');
    const coherenceScoreEl = document.getElementById('coherence-score');
    const coherenceAnalysisEl = document.getElementById('coherence-analysis');
    const benefitAnalysisEl = document.getElementById('benefit-analysis');
    const agentReflectionsContainer = document.getElementById('agent-reflections-container');
    const reflectionQuestionsContainer = document.getElementById('reflection-questions-container');
    const reflectionResponse = document.getElementById('reflection-response');
    const submitReflectionBtn = document.getElementById('submit-reflection-btn');
    const finishGameBtn = document.getElementById('finish-game-btn');
    
    // Phase indicators
    const phaseIndividual = document.getElementById('phase-individual');
    const phaseGroup = document.getElementById('phase-group');
    const phaseReflection = document.getElementById('phase-reflection');
    
    // Display a message when the page is loaded
    console.log("Page elements initialized");
    
    // Initialize game when start button is clicked
    if (startGameBtn) {
        console.log("Start game button found");
        startGameBtn.addEventListener('click', startGame);
    } else {
        console.error("Start game button not found!");
    }
    
    // Start a new game session
    async function startGame() {
        console.log("Start game button clicked");
        try {
            const response = await axios.post('/api/start-game', {});
            
            if (response.data.success) {
                console.log("Game started successfully", response.data);
                gameState.sessionId = response.data.session_id;
                gameState.agentProfiles = response.data.agent_profiles;
                gameState.currentPhase = 'individual';
                
                // Hide intro screen, show game screen
                introScreen.style.display = 'none';
                gameScreen.style.display = 'block';
                
                // Load policy areas
                loadPolicyAreas();
                
                // Display agent profiles
                displayAgentProfiles();
            }
        } catch (error) {
            console.error('Error starting game:', error);
            alert('Failed to start the game. Please try again.');
        }
    }
    
    // Load policy areas for individual phase
    async function loadPolicyAreas() {
        try {
            console.log("Loading policy areas");
            const response = await axios.get('/api/get-policy-areas');
            
            if (response.data.success) {
                const policyAreas = response.data.policy_areas;
                console.log("Policy areas loaded", policyAreas);
                
                // Clear container
                policyAreasContainer.innerHTML = '';
                
                // Add each policy area
                for (const [area, options] of Object.entries(policyAreas)) {
                    const policyCard = document.createElement('div');
                    policyCard.className = 'card mb-4';
                    
                    let optionsHtml = '';
                    
                    for (let i = 1; i <= 3; i++) {
                        const option = options[`Option ${i}`];
                        
                        optionsHtml += `
                            <div class="policy-option policy-option-${i}" data-area="${area}" data-option="${i}">
                                <h6>Option ${i} (${i} budget unit${i > 1 ? 's' : ''})</h6>
                                <p>${option}</p>
                            </div>
                        `;
                    }
                    
                    policyCard.innerHTML = `
                        <div class="card-header">
                            <h5>${area}</h5>
                        </div>
                        <div class="card-body">
                            <div class="policy-options">
                                ${optionsHtml}
                            </div>
                        </div>
                    `;
                    
                    policyAreasContainer.appendChild(policyCard);
                }
                
                // Add event listeners to policy options
                const policyOptions = document.querySelectorAll('.policy-option');
                policyOptions.forEach(option => {
                    option.addEventListener('click', function() {
                        selectPolicyOption(this);
                    });
                });
            }
        } catch (error) {
            console.error('Error loading policy areas:', error);
            alert('Failed to load policy areas. Please refresh the page.');
        }
    }
    
    // Display agent profiles
    function displayAgentProfiles() {
        console.log("Displaying agent profiles", gameState.agentProfiles);
        agentsContainer.innerHTML = '';
        
        gameState.agentProfiles.forEach(agent => {
            const agentCard = document.createElement('div');
            agentCard.className = 'col-md-3';
            agentCard.innerHTML = `
                <div class="agent-card">
                    <h5>${agent.name}</h5>
                    <p><strong>Age:</strong> ${agent.age}</p>
                    <p><strong>Education:</strong> ${agent.education}</p>
                    <p><strong>Occupation:</strong> ${agent.occupation}</p>
                    <p><strong>Status:</strong> ${agent.socioeconomic_status}</p>
                    <p><strong>Political Views:</strong> ${agent.political_stance}</p>
                </div>
            `;
            
            agentsContainer.appendChild(agentCard);
        });
        
        agentsContainer.style.display = 'flex';
    }
    
    // Select a policy option in individual phase
    async function selectPolicyOption(optionElement) {
        const area = optionElement.dataset.area;
        const option = parseInt(optionElement.dataset.option);
        
        try {
            const response = await axios.post('/api/set-preference', {
                session_id: gameState.sessionId,
                policy_area: area,
                option: option
            });
            
            if (response.data.success) {
                // Update UI to show selection
                const areaContainer = optionElement.closest('.card-body');
                const options = areaContainer.querySelectorAll('.policy-option');
                
                options.forEach(opt => {
                    opt.classList.remove('selected');
                });
                
                optionElement.classList.add('selected');
                
                // Update game state
                gameState.selectedPolicies[area] = option;
                gameState.budgetRemaining = response.data.remaining_budget;
                gameState.budgetUsed = 14 - response.data.remaining_budget;
                
                // Update budget display
                updateBudgetDisplay();
                
                // Show feedback
                if (response.data.feedback) {
                    budgetFeedbackEl.innerHTML = response.data.feedback.join('<br>');
                }
                
                // Enable proceed button if all areas selected
                if (Object.keys(gameState.selectedPolicies).length === 7) {
                    completeIndividualPhaseBtn.disabled = false;
                }
            } else {
                alert(response.data.message);
            }
        } catch (error) {
            console.error('Error selecting policy option:', error);
            alert('Failed to select policy option. Please try again.');
        }
    }
    
    // Update budget display
    function updateBudgetDisplay() {
        const percentUsed = (gameState.budgetUsed / 14) * 100;
        budgetUsedEl.style.width = `${percentUsed}%`;
        budgetDisplayEl.textContent = `${gameState.budgetUsed}/14 units used`;
    }
    
    // Complete individual phase and start group discussion
    if (completeIndividualPhaseBtn) {
        completeIndividualPhaseBtn.addEventListener('click', async function() {
            try {
                const response = await axios.post('/api/start-group-discussion', {
                    session_id: gameState.sessionId
                });
                
                if (response.data.success) {
                    // Update game state
                    gameState.currentPhase = 'group';
                    gameState.currentTopic = response.data.current_topic;
                    
                    // Update UI for group phase
                    phaseIndividual.classList.remove('active');
                    phaseIndividual.classList.add('completed');
                    phaseGroup.classList.add('active');
                    
                    individualPhase.style.display = 'none';
                    groupPhase.style.display = 'block';
                    
                    // Display current topic
                    currentTopicEl.textContent = `Current Topic: ${gameState.currentTopic}`;
                    
                    // Display opening statements
                    displayAgentStatements(response.data.statements);
                    
                    // Reset budget
                    gameState.budgetUsed = 0;
                    gameState.budgetRemaining = 14;
                    gameState.selectedPolicies = {};
                    updateBudgetDisplay();
                } else {
                    alert(response.data.message);
                }
            } catch (error) {
                console.error('Error starting group discussion:', error);
                alert('Failed to start group discussion. Please try again.');
            }
        });
    }
    
    // Display agent statements in discussion log
    function displayAgentStatements(statements) {
        statements.forEach(statement => {
            const messageEl = document.createElement('div');
            messageEl.className = 'agent-message';
            messageEl.innerHTML = `
                <p><strong>${statement.agent_name} (Option ${statement.preference}):</strong></p>
                <p>${statement.statement}</p>
            `;
            
            discussionLogEl.appendChild(messageEl);
        });
        
        // Scroll to bottom
        discussionLogEl.scrollTop = discussionLogEl.scrollHeight;
    }
    
    // Submit human argument
    if (submitArgumentBtn) {
        submitArgumentBtn.addEventListener('click', async function() {
            const argument = humanArgument.value.trim();
            const option = parseInt(humanStance.value);
            
            if (!argument) {
                alert('Please enter your argument.');
                return;
            }
            
            // Add human message to discussion log
            const messageEl = document.createElement('div');
            messageEl.className = 'human-message';
            messageEl.innerHTML = `
                <p><strong>You (Option ${option}):</strong></p>
                <p>${argument}</p>
            `;
            
            discussionLogEl.appendChild(messageEl);
            discussionLogEl.scrollTop = discussionLogEl.scrollHeight;
            
            // Clear input
            humanArgument.value = '';
            
            try {
                const response = await axios.post('/api/submit-argument', {
                    session_id: gameState.sessionId,
                    argument: argument,
                    preferred_option: option
                });
                
                if (response.data.success) {
                    // Display agent responses
                    displayAgentStatements(response.data.responses);
                }
            } catch (error) {
                console.error('Error submitting argument:', error);
                alert('Failed to submit argument. Please try again.');
            }
        });
    }
    
    // Voice input for human argument
    if (voiceInputBtn) {
        voiceInputBtn.addEventListener('click', function() {
            // This would be connected to the speech recognition API
            // For this demo, we'll just toggle the button state
            if (voiceInputBtn.classList.contains('listening')) {
                voiceInputBtn.classList.remove('listening');
                voiceInputBtn.querySelector('i').className = 'bi bi-mic';
            } else {
                voiceInputBtn.classList.add('listening');
                voiceInputBtn.querySelector('i').className = 'bi bi-mic-fill';
                
                // Simulate voice recognition result after 3 seconds
                setTimeout(() => {
                    humanArgument.value = "I believe we should prioritize comprehensive support for refugee students, even if it means higher initial costs. The long-term benefits will outweigh the short-term budget constraints.";
                    voiceInputBtn.classList.remove('listening');
                    voiceInputBtn.querySelector('i').className = 'bi bi-mic';
                }, 3000);
            }
        });
    }
    
    // Finalize option for current topic
    finalizeOptionBtns.forEach(btn => {
        btn.addEventListener('click', async function() {
            const option = parseInt(this.dataset.option);
            
            try {
                const response = await axios.post('/api/finalize-topic', {
                    session_id: gameState.sessionId,
                    option: option
                });
                
                if (response.data.success) {
                    // Update game state
                    gameState.selectedPolicies[gameState.currentTopic] = option;
                    gameState.budgetUsed = 14 - response.data.remaining_budget;
                    gameState.budgetRemaining = response.data.remaining_budget;
                    
                    // Update budget display
                    updateBudgetDisplay();
                    
                    // Add decision message to discussion log
                    const decisionEl = document.createElement('div');
                    decisionEl.className = 'alert alert-info';
                    decisionEl.innerHTML = `<strong>Decision:</strong> ${gameState.currentTopic} - Option ${option} selected.`;
                    discussionLogEl.appendChild(decisionEl);
                    discussionLogEl.scrollTop = discussionLogEl.scrollHeight;
                    
                    // Clear discussion log if moving to next topic
                    if (!response.data.is_final_topic) {
                        // Update current topic
                        gameState.currentTopic = response.data.next_topic;
                        currentTopicEl.textContent = `Current Topic: ${gameState.currentTopic}`;
                        
                        // Clear discussion log but keep decision
                        discussionLogEl.innerHTML = '';
                        discussionLogEl.appendChild(decisionEl);
                        
                        // Display opening statements for next topic
                        displayAgentStatements(response.data.statements);
                    } else {
                        // Move to reflection phase
                        startReflectionPhase();
                    }
                } else {
                    alert(response.data.message);
                }
            } catch (error) {
                console.error('Error finalizing topic:', error);
                alert('Failed to finalize topic. Please try again.');
            }
        });
    });
    
    // Start reflection phase
    async function startReflectionPhase() {
        try {
            const response = await axios.post('/api/start-reflection', {
                session_id: gameState.sessionId
            });
            
            if (response.data.success) {
                // Update game state
                gameState.currentPhase = 'reflection';
                
                // Update UI for reflection phase
                phaseGroup.classList.remove('active');
                phaseGroup.classList.add('completed');
                phaseReflection.classList.add('active');
                
                groupPhase.style.display = 'none';
                reflectionPhase.style.display = 'block';
                
                // Populate policy summary
                populatePolicySummary(response.data.final_policies);
                
                // Populate policy analysis
                populatePolicyAnalysis(response.data.policy_analysis);
                
                // Populate agent reflections
                populateAgentReflections(response.data.reflections);
                
                // Populate reflection questions
                populateReflectionQuestions(response.data.reflection_questions);
            }
        } catch (error) {
            console.error('Error starting reflection phase:', error);
            alert('Failed to start reflection phase. Please try again.');
        }
    }
    
    // Populate policy summary table
    function populatePolicySummary(policies) {
        policySummaryTable.innerHTML = '';
        let totalBudgetUsed = 0;
        
        for (const [area, option] of Object.entries(policies)) {
            const row = document.createElement('tr');
            const budgetUsed = option; // Option number equals cost
            
            row.innerHTML = `
                <td>${area}</td>
                <td>Option ${option}</td>
                <td>${budgetUsed} unit${budgetUsed > 1 ? 's' : ''}</td>
            `;
            
            policySummaryTable.appendChild(row);
            totalBudgetUsed += budgetUsed;
        }
        
        totalBudgetUsedEl.textContent = `${totalBudgetUsed} units`;
    }
    
    // Populate policy analysis
    function populatePolicyAnalysis(analysis) {
        // Set score bars
        equityScoreEl.style.width = `${analysis.equity.score * 100}%`;
        justiceScoreEl.style.width = `${analysis.justice.score * 100}%`;
        coherenceScoreEl.style.width = `${analysis.coherence.score * 100}%`;
        
        // Set analysis text
        equityAnalysisEl.textContent = analysis.equity.analysis;
        justiceAnalysisEl.textContent = analysis.justice.analysis;
        coherenceAnalysisEl.textContent = analysis.coherence.analysis;
        benefitAnalysisEl.textContent = analysis.benefit_analysis;
    }
    
    // Populate agent reflections
    function populateAgentReflections(reflections) {
        agentReflectionsContainer.innerHTML = '';
        
        reflections.forEach(reflection => {
            const reflectionEl = document.createElement('div');
            reflectionEl.className = `agent-reflection ${reflection.sentiment}`;
            reflectionEl.innerHTML = `
                <h5>${reflection.agent_name}</h5>
                <p>${reflection.reflection}</p>
                <p class="text-muted">Preference alignment: ${reflection.preference_alignment}</p>
            `;
            
            agentReflectionsContainer.appendChild(reflectionEl);
        });
    }
    
    // Populate reflection questions
    function populateReflectionQuestions(questions) {
        reflectionQuestionsContainer.innerHTML = '';
        
        questions.forEach((question, index) => {
            const questionEl = document.createElement('div');
            questionEl.className = 'reflection-question';
            questionEl.innerHTML = `
                <p><strong>Question ${index + 1}:</strong> ${question}</p>
            `;
            
            reflectionQuestionsContainer.appendChild(questionEl);
        });
    }
    
    // Submit reflection
    if (submitReflectionBtn) {
        submitReflectionBtn.addEventListener('click', async function() {
            const reflection = reflectionResponse.value.trim();
            
            if (!reflection) {
                alert('Please enter your reflection.');
                return;
            }
            
            try {
                const response = await axios.post('/api/submit-reflection', {
                    session_id: gameState.sessionId,
                    reflection_text: reflection
                });
                
                if (response.data.success) {
                    alert('Thank you for your reflection! Your responses will help improve future iterations of the CHALLENGE game.');
                    submitReflectionBtn.disabled = true;
                }
            } catch (error) {
                console.error('Error submitting reflection:', error);
                alert('Failed to submit reflection. Please try again.');
            }
        });
    }
    
    // Finish game
    if (finishGameBtn) {
        finishGameBtn.addEventListener('click', async function() {
            try {
                await axios.post('/api/clear-session', {
                    session_id: gameState.sessionId
                });
                
                alert('Thank you for playing the CHALLENGE game! We hope this experience has provided valuable insights into the complexities of refugee education policy-making.');
                
                // Reload page to restart
                window.location.reload();
            } catch (error) {
                console.error('Error finishing game:', error);
                alert('Error occurred while finishing the game.');
                window.location.reload();
            }
        });
    }
});