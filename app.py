from flask import Flask, render_template, request, jsonify
import json
import os
import random
import time
from modules.game_controller import ChallengeGameController
from modules.agent_profiles import create_random_agent_profiles

app = Flask(__name__, static_folder='static', template_folder='templates')

# Store active game sessions
game_sessions = {}

@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')

@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Start a new game session."""
    print("Start game API called")
    session_id = request.json.get('session_id', str(hash(str(os.urandom(16)))))
    
    # Create random agents for the session
    agent_profiles = create_random_agent_profiles(4)
    
    # Initialize game controller
    game_controller = ChallengeGameController(agent_profiles)
    game_sessions[session_id] = game_controller
    
    # Start the game (move to individual phase)
    result = game_controller.start_game()
    
    # Return session info
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': result['message'],
        'instructions': result['instructions'],
        'agent_profiles': agent_profiles
    })

@app.route('/api/set-preference', methods=['POST'])
def set_preference():
    """Set the human player's preference for a policy area."""
    print("Set preference API called", request.json)
    session_id = request.json.get('session_id')
    policy_area = request.json.get('policy_area')
    option = int(request.json.get('option'))
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    game_controller = game_sessions[session_id]
    result = game_controller.set_human_preference(policy_area, option)
    
    return jsonify(result)

@app.route('/api/start-group-discussion', methods=['POST'])
def start_group_discussion():
    """Start the group discussion phase."""
    print("Group discussion API called")
    session_id = request.json.get('session_id')
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    game_controller = game_sessions[session_id]
    result = game_controller.start_group_discussion()
    
    if result['success']:
        # Get opening statements from agents
        statements = game_controller.get_agent_opening_statements()
        result.update(statements)
    
    return jsonify(result)

@app.route('/api/submit-argument', methods=['POST'])
def submit_argument():
    """Submit a human argument during group discussion."""
    print("Submit argument API called")
    session_id = request.json.get('session_id')
    argument = request.json.get('argument')
    preferred_option = int(request.json.get('preferred_option'))
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    game_controller = game_sessions[session_id]
    result = game_controller.submit_human_argument(argument, preferred_option)
    
    return jsonify(result)

@app.route('/api/finalize-topic', methods=['POST'])
def finalize_topic():
    """Finalize the decision for the current topic."""
    print("Finalize topic API called")
    session_id = request.json.get('session_id')
    option = int(request.json.get('option'))
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    game_controller = game_sessions[session_id]
    result = game_controller.finalize_topic_decision(option)
    
    if result['success'] and not result.get('is_final_topic', False):
        # Get opening statements for the next topic
        statements = game_controller.get_agent_opening_statements()
        result.update(statements)
    
    return jsonify(result)

@app.route('/api/start-reflection', methods=['POST'])
def start_reflection():
    """Start the reflection phase."""
    print("Reflection API called")
    session_id = request.json.get('session_id')
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    game_controller = game_sessions[session_id]
    result = game_controller.start_reflection_phase()
    
    if result['success']:
        # Get reflections from agents
        reflections = game_controller.get_agent_reflections()
        result.update(reflections)
    
    return jsonify(result)

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate the final report."""
    print("Generate report API called")
    session_id = request.json.get('session_id')
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    game_controller = game_sessions[session_id]
    result = game_controller.generate_final_report()
    
    return jsonify(result)

@app.route('/api/get-policy-areas', methods=['GET'])
def get_policy_areas():
    """Get the list of policy areas and options."""
    print("Get policy areas API called")
    # Create a temporary controller just to get the policy areas
    temp_controller = ChallengeGameController([])
    
    return jsonify({
        'success': True,
        'policy_areas': temp_controller.policy_areas
    })

@app.route('/api/get-game-state', methods=['POST'])
def get_game_state():
    """Get the current state of the game."""
    print("Get game state API called")
    session_id = request.json.get('session_id')
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    game_controller = game_sessions[session_id]
    
    return jsonify({
        'success': True,
        'current_phase': game_controller.current_phase,
        'current_topic': game_controller.current_topic,
        'budget_used': game_controller.budget_calculator.calculate_current_usage(),
        'budget_remaining': game_controller.budget_calculator.get_remaining_budget(),
        'selected_policies': game_controller.budget_calculator.selected_policies
    })

@app.route('/api/process-speech', methods=['POST'])
def process_speech():
    """Process speech input from the user."""
    print("Process speech API called")
    session_id = request.json.get('session_id')
    speech_text = request.json.get('speech_text')
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    # In a real implementation, this would process the speech 
    # and determine the user's intent or argument
    # For now, we'll just return the text
    
    return jsonify({
        'success': True,
        'processed_text': speech_text,
        'detected_stance': detect_stance_from_text(speech_text)
    })

def detect_stance_from_text(text):
    """
    Simple function to guess the user's stance from their speech.
    This would be more sophisticated in a real implementation.
    """
    text = text.lower()
    
    # Simple keyword matching
    option3_keywords = ['comprehensive', 'inclusive', 'equal', 'rights', 'justice', 'transform']
    option2_keywords = ['moderate', 'balance', 'compromise', 'middle', 'reasonable']
    option1_keywords = ['minimal', 'cost', 'budget', 'restrict', 'limit', 'control']
    
    option3_score = sum(1 for keyword in option3_keywords if keyword in text)
    option2_score = sum(1 for keyword in option2_keywords if keyword in text)
    option1_score = sum(1 for keyword in option1_keywords if keyword in text)
    
    if option3_score > option2_score and option3_score > option1_score:
        return 3
    elif option2_score > option3_score and option2_score > option1_score:
        return 2
    elif option1_score > option3_score and option1_score > option2_score:
        return 1
    else:
        return 2  # Default to middle option if unclear

@app.route('/api/submit-reflection', methods=['POST'])
def submit_reflection():
    """Submit the user's reflection responses."""
    print("Submit reflection API called")
    session_id = request.json.get('session_id')
    reflection_text = request.json.get('reflection_text')
    
    if session_id not in game_sessions:
        return jsonify({'success': False, 'message': 'Invalid session ID'})
    
    # In a real implementation, this would store the reflection
    # For now, we'll just acknowledge receipt
    
    return jsonify({
        'success': True,
        'message': 'Reflection received. Thank you for your thoughtful response.'
    })

@app.route('/api/clear-session', methods=['POST'])
def clear_session():
    """Clear a game session when the player exits."""
    print("Clear session API called")
    session_id = request.json.get('session_id')
    
    if session_id in game_sessions:
        del game_sessions[session_id]
    
    return jsonify({
        'success': True,
        'message': 'Session cleared'
    })

if __name__ == '__main__':
    print("Starting CHALLENGE Game server...")
    app.run(debug=True)