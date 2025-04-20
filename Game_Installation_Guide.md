# CHALLENGE Game Installation Guide

This guide provides step-by-step instructions for installing and running the CHALLENGE Game simulation on your local machine.

## Prerequisites

Before installing the CHALLENGE Game, ensure you have the following:

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)
- A modern web browser (Chrome, Firefox, Safari, or Edge)

## Installation Steps

### 1. Set Up the Project Directory

First, create and navigate to a project directory:

```bash
# Create a directory for the project
mkdir -p ~/challenge-game
cd ~/challenge-game
```

### 2. Install Required Dependencies

Create a virtual environment and install the required dependencies:

```bash
# Create a virtual environment
python -m venv venv

source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Set Up the Project Structure

Create the necessary directories and files:

```bash
# Create project structure
mkdir -p static/css static/js templates modules
```

### 4. Verify Directory Structure

Your directory structure should look like this:

```
~/challenge-game/
├── app.py
├── modules/
│   ├── __init__.py
│   ├── agent_policy_preferences.py
│   ├── agent_profiles.py
│   ├── agent_response_generator.py
│   ├── budget_calculator.py
│   ├── game_controller.py
│   └── voice_integration.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── game.js
├── templates/
│   └── index.html
└── venv/
```

### 5. Run the Application

Start the Flask application:

```bash
# Make sure your virtual environment is activated
python app.py
```

You should see output indicating that the Flask server is running, typically on http://localhost:5000.

### 6. Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

You should now see the CHALLENGE Game welcome screen.

## Troubleshooting

If you encounter issues during installation or while running the application, try these solutions:

### Problem: ImportError for modules

**Solution**: Make sure all module files are in the correct location and that the `__init__.py` file exists in the modules directory.

### Problem: 404 errors for static files

**Solution**: Verify that your CSS and JavaScript files are in the correct directories:
- CSS files should be in `static/css/`
- JavaScript files should be in `static/js/`

### Problem: "Start Game" button doesn't work

**Solution**: 
1. Check the browser console (F12) for JavaScript errors
2. Verify that Axios is loaded correctly in your HTML file
3. Ensure that the event listeners are properly set up in game.js

### Problem: Flask server won't start

**Solution**:
1. Check if another process is already using port 5000
2. Verify your Python version (3.8+ required)
3. Ensure all dependencies are installed correctly

## Next Steps

After successfully installing and running the CHALLENGE Game, consider:

1. Reading the User Manual to understand game mechanics and features
2. Exploring the codebase to learn how different components interact
3. Modifying the game parameters to create custom scenarios

For additional assistance, refer to the User Manual.

Happy gaming!