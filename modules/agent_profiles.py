import random

def create_random_agent_profiles(num_agents=4):
    """
    Generate random profiles for AI agents with diverse backgrounds.
    
    Parameters:
    - num_agents: Number of agents to create (default: 4)
    
    Returns:
    - List of agent profile dictionaries
    """
    # Lists of possible values for each attribute
    first_names = [
        "Alex", "Jordan", "Morgan", "Taylor", "Casey", "Quinn", "Riley", "Avery",
        "Cameron", "Hayden", "Reese", "Finley", "Dakota", "Robin", "Harper", "Emerson"
    ]
    
    ages = list(range(25, 71))  # Ages 25-70
    
    education_levels = [
        "High School Diploma",
        "Technical Certificate",
        "Associate's Degree",
        "Bachelor's Degree in Humanities",
        "Bachelor's Degree in Social Sciences",
        "Bachelor's Degree in Business",
        "Bachelor's Degree in STEM",
        "Master's Degree in Education",
        "Master's Degree in Public Policy",
        "Master's Degree in Social Work",
        "Master's Degree in Business Administration",
        "PhD in Economics",
        "PhD in Political Science",
        "PhD in Sociology",
        "PhD in Education"
    ]
    
    occupations = [
        "Teacher",
        "School Administrator", 
        "University Professor",
        "Civil Servant",
        "NGO Worker",
        "Social Worker",
        "Lawyer",
        "Small Business Owner",
        "Corporate Executive",
        "Healthcare Professional",
        "Community Organizer",
        "Journalist",
        "Religious Leader",
        "Retired Military Officer",
        "Local Government Official"
    ]
    
    socioeconomic_statuses = [
        "Working class",
        "Lower middle class",
        "Middle class",
        "Upper middle class",
        "Affluent"
    ]
    
    political_stances = [
        "Conservative",
        "Moderate conservative",
        "Moderate",
        "Moderate liberal",
        "Liberal",
        "Progressive",
        "Socialist",
        "Libertarian",
        "Centrist",
        "Pragmatist"
    ]
    
    # Ensure no duplicate names
    chosen_names = random.sample(first_names, num_agents)
    
    # Create a list to hold agent profiles
    agent_profiles = []
    
    for i in range(num_agents):
        # Make age and education somewhat correlated
        age = random.choice(ages)
        if age < 30:
            education_possibilities = education_levels[:7]  # Limit younger agents to lower education levels
        elif age < 40:
            education_possibilities = education_levels[:12]  # Mid-age can have up to masters
        else:
            education_possibilities = education_levels  # Older can have any education level
        
        # Make occupation somewhat correlated with education
        education = random.choice(education_possibilities)
        if "PhD" in education:
            occupation_possibilities = ["University Professor", "NGO Worker", "Corporate Executive", "Local Government Official"]
        elif "Master's" in education:
            occupation_possibilities = ["School Administrator", "University Professor", "Civil Servant", "NGO Worker", "Corporate Executive", "Healthcare Professional", "Lawyer"]
        else:
            occupation_possibilities = occupations
            
        # Create agent profile
        agent_profile = {
            "id": f"agent_{i+1}",
            "name": chosen_names[i],
            "age": age,
            "education": education,
            "occupation": random.choice(occupation_possibilities),
            "socioeconomic_status": random.choice(socioeconomic_statuses),
            "political_stance": random.choice(political_stances)
        }
        
        agent_profiles.append(agent_profile)
    
    # Ensure diversity in political stances
    # Make sure we have at least one agent from each major political category
    political_categories = ["Conservative", "Moderate", "Liberal/Progressive"]
    has_category = {category: False for category in political_categories}
    
    for agent in agent_profiles:
        stance = agent["political_stance"]
        if "Conservative" in stance:
            has_category["Conservative"] = True
        elif "Moderate" in stance:
            has_category["Moderate"] = True
        elif "Liberal" in stance or "Progressive" in stance or "Socialist" in stance:
            has_category["Liberal/Progressive"] = True
    
    # If any category is missing, adjust an agent to fill it
    for i, category in enumerate([cat for cat, has in has_category.items() if not has]):
        if i < len(agent_profiles):
            if category == "Conservative":
                agent_profiles[i]["political_stance"] = "Conservative"
            elif category == "Moderate":
                agent_profiles[i]["political_stance"] = "Moderate"
            elif category == "Liberal/Progressive":
                agent_profiles[i]["political_stance"] = "Liberal"
    
    return agent_profiles

# Example usage:
# profiles = create_random_agent_profiles(4)
# print(profiles)