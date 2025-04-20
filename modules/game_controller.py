from modules.agent_policy_preferences import generate_all_agent_preferences
from modules.agent_response_generator import AgentResponseGenerator
from modules.budget_calculator import BudgetCalculator
import random
import json
import time

class ChallengeGameController:
    def __init__(self, agent_profiles):
        """Initialize the game controller with agent profiles."""
        self.agent_profiles = agent_profiles
        self.agent_preferences = generate_all_agent_preferences(agent_profiles)
        self.response_generator = AgentResponseGenerator()
        self.budget_calculator = BudgetCalculator()
        self.discussion_history = []
        self.human_preferences = {}
        self.current_phase = "setup"  # setup, individual, group, reflection
        self.current_topic = None
        
        # Policy areas and their descriptions
        self.policy_areas = {
            "Access to Education": {
                "Option 1": "Limit access to education for refugees, allowing only a small percentage to enroll in mainstream schools.",
                "Option 2": "Establish separate schools or learning centers specifically for refugee education.",
                "Option 3": "Provide equal access to education for all, and integrate refugee students into mainstream schools."
            },
            "Language Instruction": {
                "Option 1": "Maintain the current policy of teaching only Teanish in schools.",
                "Option 2": "Provide primary Teanish language courses to refugees.",
                "Option 3": "Implement comprehensive bilingual education programs."
            },
            "Teacher Training": {
                "Option 1": "Provide minimal or no specific training for teachers regarding refugee education.",
                "Option 2": "Offer basic training sessions for teachers to familiarize them with refugee needs.",
                "Option 3": "Implement comprehensive and ongoing training programs for teachers."
            },
            "Curriculum Adaptation": {
                "Option 1": "Maintain the existing national curriculum without modifications.",
                "Option 2": "Introduce supplementary materials that acknowledge refugee experiences.",
                "Option 3": "Adapt the national curriculum to include diverse perspectives and cultural elements."
            },
            "Psychosocial Support": {
                "Option 1": "Provide limited or no specific psychosocial support for refugee students.",
                "Option 2": "Establish basic support services such as counseling and peer support programs.",
                "Option 3": "Develop comprehensive and specialized psychosocial support programs."
            },
            "Financial Support": {
                "Option 1": "Allocate minimal funds to support refugee education.",
                "Option 2": "Increase financial support for refugee education, though still insufficient.",
                "Option 3": "Allocate significant financial resources to ensure adequate funding."
            },
            "Certification/Accreditation": {
                "Option 1": "Only recognize educational qualifications obtained within the Republic of Bean.",
                "Option 2": "Establish a comprehensive evaluation process for previous educational experiences.",
                "Option 3": "Develop tailored programs that combine recognition with additional training."
            }
        }
    
    def start_game(self):
        """Start the game and move to the individual decision phase."""
        self.current_phase = "individual"
        return {
            "message": "Welcome to the CHALLENGE Game! You are now in the Individual Decision-Making Phase.",
            "instructions": "Please review the policy options and make your individual selections while staying within the 14-unit budget."
        }
    
    def set_human_preference(self, policy_area, option):
        """Set the human player's preference for a policy area."""
        if self.current_phase != "individual":
            return {"success": False, "message": "You can only set preferences in the Individual Decision-Making Phase."}
        
        if policy_area not in self.policy_areas:
            return {"success": False, "message": f"Invalid policy area: {policy_area}"}
        
        if option not in [1, 2, 3]:
            return {"success": False, "message": f"Invalid option: {option}. Must be 1, 2, or 3."}
        
        # Try to set the policy option
        success = self.budget_calculator.set_policy_option(policy_area, option)
        
        if success:
            self.human_preferences[policy_area] = option
            remaining_budget = self.budget_calculator.get_remaining_budget()
            return {
                "success": True, 
                "message": f"Preference set for {policy_area}: Option {option}.",
                "remaining_budget": remaining_budget,
                "feedback": self.budget_calculator.get_feedback()
            }
        else:
            return {
                "success": False, 
                "message": "Not enough budget to select this option.",
                "remaining_budget": self.budget_calculator.get_remaining_budget()
            }
    
    def start_group_discussion(self):
        """Start the group discussion phase."""
        if self.current_phase != "individual":
            return {"success": False, "message": "You must complete the Individual Decision-Making Phase first."}
            
        # Check if the human has made decisions for all policy areas
        policy_summary = self.budget_calculator.get_policy_summary()
        if not policy_summary["has_complete_policy_set"]:
            return {
                "success": False, 
                "message": "You must make decisions for all policy areas before starting the group discussion.",
                "feedback": self.budget_calculator.get_feedback()
            }
        
        self.current_phase = "group"
        self.current_topic = list(self.policy_areas.keys())[0]  # Start with first policy area
        
        # Reset the budget calculator for the group phase
        self.budget_calculator = BudgetCalculator()
        
        return {
            "success": True,
            "message": "Welcome to the Group Discussion Phase! The AI agents will now debate the policy options with you.",
            "current_topic": self.current_topic,
            "instructions": "Discuss with the AI agents to reach a consensus on each policy area."
        }
    
    def get_agent_opening_statements(self):
        """Get opening statements from all agents for the current topic."""
        if self.current_phase != "group":
            return {"success": False, "message": "Not in the Group Discussion Phase."}
        
        statements = []
        for agent in self.agent_profiles:
            agent_id = agent["id"]
            preference = self.agent_preferences[agent_id][self.current_topic]
            
            response = self.response_generator.generate_response(
                agent,
                self.current_topic,
                preference,
                "",  # No discussion yet
                self.budget_calculator.get_remaining_budget()
            )
            
            statements.append({
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "preference": preference,
                "statement": response
            })
            
            # Add to discussion history
            self.discussion_history.append({
                "phase": "group",
                "topic": self.current_topic,
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "statement": response,
                "timestamp": time.time()
            })
        
        return {
            "success": True,
            "topic": self.current_topic,
            "statements": statements
        }
    
    def submit_human_argument(self, argument, preferred_option):
        """Process a human argument during the group discussion."""
        if self.current_phase != "group":
            return {"success": False, "message": "Not in the Group Discussion Phase."}
        
        # Record human argument
        self.discussion_history.append({
            "phase": "group",
            "topic": self.current_topic,
            "agent_id": "human",
            "agent_name": "Human Player",
            "statement": argument,
            "timestamp": time.time()
        })
        
        # Generate responses from agents
        responses = []
        for agent in self.agent_profiles:
            agent_id = agent["id"]
            agent_preference = self.agent_preferences[agent_id][self.current_topic]
            
            # Generate a counterargument based on the agent's stance
            response = self.response_generator.generate_debate_argument(
                agent,
                self.current_topic,
                agent_preference,
                preferred_option
            )
            
            responses.append({
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "statement": response
            })
            
            # Add to discussion history
            self.discussion_history.append({
                "phase": "group",
                "topic": self.current_topic,
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "statement": response,
                "timestamp": time.time()
            })
        
        return {
            "success": True,
            "topic": self.current_topic,
            "responses": responses
        }
    
    def finalize_topic_decision(self, option):
        """Finalize the decision for the current topic and move to the next one."""
        if self.current_phase != "group":
            return {"success": False, "message": "Not in the Group Discussion Phase."}
        
        # Try to set the policy option
        success = self.budget_calculator.set_policy_option(self.current_topic, option)
        
        if not success:
            return {
                "success": False, 
                "message": "Not enough budget to select this option.",
                "remaining_budget": self.budget_calculator.get_remaining_budget()
            }
        
        # Record the decision
        self.discussion_history.append({
            "phase": "group",
            "topic": self.current_topic,
            "decision": option,
            "timestamp": time.time()
        })
        
        # Move to the next topic
        current_index = list(self.policy_areas.keys()).index(self.current_topic)
        if current_index < len(self.policy_areas) - 1:
            self.current_topic = list(self.policy_areas.keys())[current_index + 1]
            return {
                "success": True,
                "message": f"Decision for {self.current_topic} set to Option {option}. Moving to next topic: {self.current_topic}",
                "next_topic": self.current_topic,
                "remaining_budget": self.budget_calculator.get_remaining_budget(),
                "is_final_topic": False
            }
        else:
            # This was the last topic
            self.current_phase = "reflection"
            return {
                "success": True,
                "message": f"Decision for {self.current_topic} set to Option {option}. All topics have been decided.",
                "remaining_budget": self.budget_calculator.get_remaining_budget(),
                "is_final_topic": True,
                "next_phase": "reflection"
            }
    
    def start_reflection_phase(self):
        """Start the reflection phase with analysis of decisions."""
        if self.current_phase != "reflection":
            return {"success": False, "message": "You must complete the Group Discussion Phase first."}
        
        # Check if all decisions have been made
        policy_summary = self.budget_calculator.get_policy_summary()
        if not policy_summary["has_complete_policy_set"]:
            return {
                "success": False, 
                "message": "You must make decisions for all policy areas before starting the reflection phase."
            }
        
        # Generate reflection questions
        reflection_questions = [
            "What emotions came up for you during the decision-making process—discomfort, frustration, detachment, guilt? What do those feelings reveal about your position in relation to refugee education?",
            "How did the group dynamics impact your ability to advocate for certain policies? Were there moments when you chose silence or compromise? Why?",
            "Whose interests did your decisions ultimately serve—refugees, citizens, or the state? Why?",
            "What compromises did you make for the sake of consensus, and who or what got erased in the process?",
            "How did the structure of the game (budget, options, scenario) shape or limit your imagination of justice?"
        ]
        
        # Analyze the policy decisions
        final_policies = self.budget_calculator.selected_policies
        policy_analysis = self._analyze_policy_package(final_policies)
        
        return {
            "success": True,
            "message": "Welcome to the Reflection Phase! Let's analyze the decisions made and their implications.",
            "final_policies": final_policies,
            "policy_analysis": policy_analysis,
            "reflection_questions": reflection_questions,
            "budget_used": self.budget_calculator.calculate_current_usage(),
            "budget_remaining": self.budget_calculator.get_remaining_budget()
        }
    
    def _analyze_policy_package(self, policies):
        """Analyze the chosen policy package for equity, justice, and coherence."""
        # Count policy levels
        level_counts = {1: 0, 2: 0, 3: 0}
        for area, option in policies.items():
            level_counts[option] += 1
        
        # Calculate equity score (higher = more equitable)
        equity_score = (level_counts[3] * 3 + level_counts[2] * 2 + level_counts[1]) / 7
        
        # Calculate justice score based on certain critical areas
        justice_critical_areas = {
            "Access to Education": policies["Access to Education"],
            "Psychosocial Support": policies["Psychosocial Support"],
            "Certification/Accreditation": policies["Certification/Accreditation"]
        }
        justice_score = sum(justice_critical_areas.values()) / (3 * 3)  # Max possible is 1.0
        
        # Calculate coherence (are policy choices aligned?)
        coherence_pairs = [
            ("Access to Education", "Language Instruction"),
            ("Teacher Training", "Curriculum Adaptation"),
            ("Financial Support", "Psychosocial Support")
        ]
        
        coherence_score = 0
        for area1, area2 in coherence_pairs:
            # Closer options = more coherent
            difference = abs(policies[area1] - policies[area2])
            if difference == 0:
                coherence_score += 1
            elif difference == 1:
                coherence_score += 0.5
        coherence_score = coherence_score / len(coherence_pairs)
        
        # Overall analysis
        if equity_score > 0.7:
            equity_analysis = "Your policy package strongly prioritizes equity and inclusion."
        elif equity_score > 0.5:
            equity_analysis = "Your policy package shows a moderate commitment to equity."
        else:
            equity_analysis = "Your policy package prioritizes minimal intervention over equity concerns."
            
        if justice_score > 0.7:
            justice_analysis = "Your decisions strongly support justice-oriented approaches to refugee education."
        elif justice_score > 0.5:
            justice_analysis = "Your decisions show some commitment to justice but with significant compromises."
        else:
            justice_analysis = "Your decisions prioritize system stability over transformative justice."
            
        if coherence_score > 0.7:
            coherence_analysis = "Your policy choices are highly coherent and mutually reinforcing."
        elif coherence_score > 0.5:
            coherence_analysis = "Your policy choices show moderate coherence with some contradictions."
        else:
            coherence_analysis = "Your policy choices contain significant contradictions that may undermine effectiveness."
        
        # Identify who benefits most
        benefit_analysis = ""
        if equity_score < 0.4:
            benefit_analysis = "Your policy package primarily serves the interests of the state and existing citizens."
        elif justice_score > 0.7 and equity_score > 0.6:
            benefit_analysis = "Your policy package strongly centers refugee needs and rights."
        else:
            benefit_analysis = "Your policy package attempts to balance state interests with some refugee needs."
        
        return {
            "equity": {
                "score": equity_score,
                "analysis": equity_analysis
            },
            "justice": {
                "score": justice_score,
                "analysis": justice_analysis
            },
            "coherence": {
                "score": coherence_score,
                "analysis": coherence_analysis
            },
            "benefit_analysis": benefit_analysis,
            "statistics": {
                "option_distribution": level_counts,
                "budget_used": self.budget_calculator.calculate_current_usage(),
                "budget_remaining": self.budget_calculator.get_remaining_budget()
            }
        }
    
    def get_agent_reflections(self):
        """Get reflective comments from AI agents on the final policy package."""
        if self.current_phase != "reflection":
            return {"success": False, "message": "Not in the Reflection Phase."}
        
        final_policies = self.budget_calculator.selected_policies
        reflections = []
        
        for agent in self.agent_profiles:
            agent_id = agent["id"]
            
            # Count how many of the agent's preferences were honored
            preference_alignment = 0
            for area, option in final_policies.items():
                if self.agent_preferences[agent_id][area] == option:
                    preference_alignment += 1
            
            alignment_percentage = (preference_alignment / 7) * 100
            
            # Generate a reflective comment
            if alignment_percentage > 70:
                sentiment = "satisfied"
                reflection = f"I'm pleased with our final policy package as it aligns with many of my priorities. Particularly, I appreciate our approach to {list(final_policies.keys())[preference_alignment-1]}."
            elif alignment_percentage > 40:
                sentiment = "mixed"
                # Find an area where the agent's preference wasn't followed
                disagreement_area = ""
                for area, option in final_policies.items():
                    if self.agent_preferences[agent_id][area] != option:
                        disagreement_area = area
                        break
                        
                reflection = f"The final policy has some strengths, but I'm disappointed in our decision on {disagreement_area}. I believe we could have done better there."
            else:
                sentiment = "disappointed"
                reflection = "This policy package falls short of what I believe would truly serve the refugee population. Too many compromises were made at the expense of those most vulnerable."
            
            reflections.append({
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "sentiment": sentiment,
                "reflection": reflection,
                "preference_alignment": f"{alignment_percentage:.1f}%"
            })
        
        return {
            "success": True,
            "reflections": reflections
        }
    
    def generate_final_report(self):
        """Generate a comprehensive final report on the game outcomes."""
        if self.current_phase != "reflection":
            return {"success": False, "message": "Not in the Reflection Phase."}
            
        final_policies = self.budget_calculator.selected_policies
        policy_analysis = self._analyze_policy_package(final_policies)
        
        # Analyze the discussion dynamics
        discussion_analysis = self._analyze_discussion_dynamics()
        
        return {
            "success": True,
            "final_policies": final_policies,
            "policy_analysis": policy_analysis,
            "discussion_analysis": discussion_analysis,
            "budget_summary": {
                "total_budget": self.budget_calculator.total_budget,
                "used_budget": self.budget_calculator.calculate_current_usage(),
                "remaining_budget": self.budget_calculator.get_remaining_budget()
            }
        }
    
    def _analyze_discussion_dynamics(self):
        """Analyze the dynamics of the group discussion phase."""
        # This would be more sophisticated in a full implementation
        # Here's a simplified version
        
        # Count contributions by each agent
        contribution_counts = {"human": 0}
        for agent in self.agent_profiles:
            contribution_counts[agent["id"]] = 0
            
        for entry in self.discussion_history:
            if entry.get("agent_id") and "statement" in entry:
                contribution_counts[entry["agent_id"]] += 1
        
        # Identify dominant voices
        max_contributions = max(contribution_counts.values())
        dominant_voices = [agent_id for agent_id, count in contribution_counts.items() 
                          if count > 0.7 * max_contributions]
        
        # Identify silenced voices
        min_contributions = min(contribution_counts.values())
        silenced_voices = [agent_id for agent_id, count in contribution_counts.items() 
                          if count < 0.3 * max_contributions and count > 0]
        
        return {
            "contribution_counts": contribution_counts,
            "dominant_voices": dominant_voices,
            "silenced_voices": silenced_voices,
            "total_exchanges": len([e for e in self.discussion_history if "statement" in e])
        }