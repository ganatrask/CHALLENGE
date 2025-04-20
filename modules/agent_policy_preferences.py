import random

def generate_policy_preferences(agent_profile):
    """
    Generate policy preferences for an agent based on their profile.
    Returns a dictionary with the agent's preferred option (1-3) for each policy area.
    """
    preferences = {}
    
    # Define tendency based on political stance
    stance = agent_profile["political_stance"]
    if stance == "Conservative":
        # Conservative agents tend to prefer option 1 (more restrictive)
        base_tendency = 1.3
    elif stance == "Moderate":
        # Moderate agents tend to prefer option 2 (middle ground)
        base_tendency = 2.0
    elif stance == "Liberal":
        # Liberal agents tend to prefer options 2-3 (more inclusive)
        base_tendency = 2.3
    elif stance == "Socialist":
        # Socialist agents tend to prefer option 3 (most inclusive)
        base_tendency = 2.7
    else:
        base_tendency = 2.0
    
    # Adjust tendency based on occupation
    occupation = agent_profile["occupation"]
    if occupation in ["NGO Worker", "Teacher", "Social Worker"]:
        # These occupations may favor more inclusive policies
        base_tendency += 0.3
    elif occupation in ["Civil Servant", "University Professor"]:
        # These occupations may be more balanced
        base_tendency += 0.1
    elif occupation in ["Business Owner", "Corporate Executive"]:
        # These occupations may favor more restrictive policies
        base_tendency -= 0.2
        
    # Generate preferences for each policy area
    policy_areas = [
        "Access to Education", 
        "Language Instruction", 
        "Teacher Training", 
        "Curriculum Adaptation",
        "Psychosocial Support", 
        "Financial Support", 
        "Certification/Accreditation"
    ]
    
    # Create some special interest areas based on agent profile
    if agent_profile["education"].startswith("PhD") or agent_profile["education"].startswith("Master"):
        special_interests = [random.choice(policy_areas)]  # Educated agents have one special interest
    else:
        special_interests = []
    
    # NGO workers care about psychosocial support
    if occupation == "NGO Worker":
        special_interests.append("Psychosocial Support")
    
    # Civil servants care about certification
    if occupation == "Civil Servant":
        special_interests.append("Certification/Accreditation")
    
    # Professors care about curriculum
    if occupation == "University Professor":
        special_interests.append("Curriculum Adaptation")
    
    # Add some randomization to make agents less predictable
    for policy in policy_areas:
        # Base calculation
        preference_value = base_tendency
        
        # Adjust for special interests (higher option number = more progressive)
        if policy in special_interests:
            preference_value += 0.5
            
        # Add some randomness
        preference_value += random.uniform(-0.5, 0.5)
        
        # Convert to option 1, 2, or 3
        if preference_value < 1.5:
            preferences[policy] = 1
        elif preference_value < 2.5:
            preferences[policy] = 2
        else:
            preferences[policy] = 3
    
    return preferences

def generate_all_agent_preferences(agent_profiles):
    """Generate preferences for all agents."""
    all_preferences = {}
    for agent in agent_profiles:
        all_preferences[agent["id"]] = generate_policy_preferences(agent)
    return all_preferences

# Example usage:
# all_agent_preferences = generate_all_agent_preferences(agent_profiles)
# print(all_agent_preferences)