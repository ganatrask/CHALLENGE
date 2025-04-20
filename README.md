# CHALLENGE Game - User Manual

## Introduction

Welcome to the CHALLENGE (Creating Holistic Approaches for Learning, Liberty, and Equity in New Global Education) Game, an educational simulation that explores refugee education policy-making. This interactive experience places you in the role of a parliament member in the fictional Republic of Bean, tasked with developing education policies for refugee populations.

This user manual will guide you through the features, gameplay mechanics, and technical requirements of the CHALLENGE Game.

## Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Game Phases](#game-phases)
   - [Phase 1: Individual Decision-Making](#phase-1-individual-decision-making)
   - [Phase 2: Group Discussion](#phase-2-group-discussion)
   - [Phase 3: Reflection](#phase-3-reflection)
5. [Game Mechanics](#game-mechanics)
   - [Budget System](#budget-system)
   - [Policy Options](#policy-options)
   - [AI Agents](#ai-agents)
6. [Features](#features)
   - [Voice Interaction](#voice-interaction)
   - [Real-time Budget Tracking](#real-time-budget-tracking)
   - [Analysis and Reflection](#analysis-and-reflection)
7. [Technical Support](#technical-support)

## Overview

The CHALLENGE Game simulates the complex process of creating education policies for refugees. Set in the fictional Republic of Bean, which has recently received two million refugees (14% of its population) from neighboring Orangenya, you must work with AI parliament colleagues to develop a comprehensive education policy package.

The game is designed to:
- Highlight the ethical dimensions of refugee education policy
- Demonstrate the real-world constraints and trade-offs in policymaking
- Encourage critical reflection on power, privilege, and justice in education
- Provide an immersive experience through AI-simulated colleagues

## System Requirements

- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest version recommended)
- **Internet Connection**: Stable connection required
- **Screen Resolution**: Minimum 1280x720
- **Audio**: Speakers or headphones (for voice interaction)
- **Microphone**: Optional (for voice input feature)

## Installation

The CHALLENGE Game is a web-based application that requires Python and Flask to run locally. Follow these steps to install and run the game:

1. Ensure you have Python 3.8 or higher installed
2. Clone or download the CHALLENGE Game repository
3. Navigate to the project directory
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Start the Flask server:
   ```
   python app.py
   ```
6. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Game Phases

The CHALLENGE Game consists of three distinct phases, each designed to simulate a different aspect of the policymaking process.

### Phase 1: Individual Decision-Making

In this initial phase, you'll make individual policy choices across seven key areas:

1. **Access to Education**: Determine how refugee students will access schooling
2. **Language Instruction**: Choose language teaching approaches
3. **Teacher Training**: Decide on teacher preparation for refugee education
4. **Curriculum Adaptation**: Select curriculum modifications
5. **Psychosocial Support**: Choose mental health support options
6. **Financial Support**: Allocate financial resources
7. **Certification/Accreditation**: Determine how to recognize prior education

For each policy area, you'll select one of three options (costing 1, 2, or 3 budget units) while staying within a total budget of 14 units.

**Key Features in This Phase:**
- Interactive policy selection interface
- Real-time budget tracking
- Policy option descriptions with advantages and disadvantages
- Visual indication of selected policies

### Phase 2: Group Discussion

After making your individual choices, you'll enter the group discussion phase where you debate policy options with four AI parliament colleagues. Each AI agent has unique backgrounds, education levels, occupations, and political stances that influence their policy preferences.

During this phase, you'll:
- Discuss each policy area one at a time
- Read AI agents' arguments and perspectives
- Submit your own arguments via text or voice
- Make final decisions for each policy area

**Key Features in This Phase:**
- Dynamic discussion with AI agents
- Voice input option for arguments
- Real-time responses from AI colleagues
- Sequential consideration of all seven policy areas

### Phase 3: Reflection

The final phase encourages critical reflection on the policymaking process and outcomes. The system will analyze your final policy package and provide metrics on:

- **Equity Score**: How equitable your policies are
- **Justice Score**: How well your policies serve justice
- **Coherence Score**: How well your policies work together
- **Benefit Analysis**: Who benefits most from your policy package

You'll also see reflections from your AI colleagues on the final policy package and can respond to guided reflection questions.

**Key Features in This Phase:**
- Policy package summary
- Analytical scoring of your decisions
- AI agent reflections
- Guided reflection questions
- Opportunity to submit your own reflection

## Game Mechanics

### Budget System

The budget system is a central mechanic that simulates real-world resource constraints:

- Total budget: 14 units
- Option costs: Option 1 costs 1 unit, Option 2 costs 2 units, Option 3 costs 3 units
- You must allocate all 14 units across the seven policy areas
- The game enforces the budget limit and provides real-time feedback

### Policy Options

Each policy area offers three options with increasing costs and benefits:

- **Option 1 (1 unit)**: Minimal intervention, typically focused on maintaining existing systems
- **Option 2 (2 units)**: Moderate changes that provide some support for refugees
- **Option 3 (3 units)**: Transformative approaches that prioritize inclusion and equity

Each option comes with advantages and disadvantages, requiring you to make trade-offs based on your priorities and available budget.

### AI Agents

The four AI parliament colleagues are procedurally generated with unique profiles:

- **Age**: Ranging from 25 to 70
- **Education**: Various levels from high school to PhD
- **Occupation**: Different professional backgrounds
- **Socioeconomic Status**: Working class to affluent
- **Political Stance**: Conservative to progressive

These characteristics influence their policy preferences and arguments during the group discussion phase. The agents can agree, disagree, and compromise based on their values and the arguments presented.

## Features

### Voice Interaction

The CHALLENGE Game offers optional voice interaction:

- **Voice Input**: Click the microphone button to speak your arguments instead of typing
- **Automatic Speech Processing**: The system interprets your spoken arguments and determines your stance
- **Natural Interaction**: Creates a more immersive debate experience

### Real-time Budget Tracking

The budget tracking system provides immediate feedback on your resource allocation:

- **Visual Budget Bar**: Shows how much of your budget is used
- **Numerical Display**: Shows units used and remaining
- **Feedback Messages**: Provides guidance on budget usage
- **Enforcement**: Prevents exceeding the 14-unit limit

### Analysis and Reflection

The game includes sophisticated analysis tools:

- **Policy Scoring**: Evaluates your policy package on equity, justice, and coherence
- **Visual Score Indicators**: Graphical representation of your scores
- **AI Agent Reflections**: Generated responses from your colleagues
- **Guided Reflection Questions**: Prompts for deeper thinking about the experience

## Technical Support

If you encounter any issues while running the CHALLENGE Game:

1. Check the browser console (F12) for error messages
2. Verify that all files are in the correct directory structure
3. Ensure all dependencies are installed
4. Check that the Flask server is running properly

---

We hope this user manual helps you navigate the CHALLENGE Game effectively. Remember, the goal of this simulation is not just to "win" but to engage thoughtfully with the complex ethical and practical dimensions of refugee education policy.

As you play, consider whose voices are amplified or silenced in your decisions, who benefits from your policies, and how structures of power and privilege shape the education landscape. These reflections are the true learning outcomes of the CHALLENGE experience.

Thank you for participating in this educational simulation!