class BudgetCalculator:
    def __init__(self, total_budget=14):
        """Initialize with the total available budget (default: 14 units)."""
        self.total_budget = total_budget
        self.policy_costs = {
            "Option 1": 1,
            "Option 2": 2,
            "Option 3": 3
        }
        self.policy_areas = [
            "Access to Education", 
            "Language Instruction", 
            "Teacher Training", 
            "Curriculum Adaptation",
            "Psychosocial Support", 
            "Financial Support", 
            "Certification/Accreditation"
        ]
        # Initialize selected policies dict
        self.selected_policies = {}
        for area in self.policy_areas:
            self.selected_policies[area] = None
    
    def calculate_current_usage(self):
        """Calculate how much budget is currently used."""
        total_used = 0
        for area, option in self.selected_policies.items():
            if option is not None:
                total_used += self.policy_costs[f"Option {option}"]
        return total_used
    
    def get_remaining_budget(self):
        """Get the remaining available budget."""
        return self.total_budget - self.calculate_current_usage()
    
    def can_afford_option(self, option):
        """Check if a specific option can be afforded with the remaining budget."""
        cost = self.policy_costs[f"Option {option}"]
        return cost <= self.get_remaining_budget()
    
    def set_policy_option(self, area, option):
        """
        Set a policy option for a specific area.
        Returns True if successful, False if budget would be exceeded.
        """
        if area not in self.policy_areas:
            raise ValueError(f"Invalid policy area: {area}")
        
        if option not in [1, 2, 3]:
            raise ValueError(f"Invalid option: {option}. Must be 1, 2, or 3.")
        
        # Calculate new budget usage
        current_option = self.selected_policies[area]
        current_cost = 0 if current_option is None else self.policy_costs[f"Option {current_option}"]
        new_cost = self.policy_costs[f"Option {option}"]
        
        # Check if we can afford the change
        budget_change = new_cost - current_cost
        if self.get_remaining_budget() < budget_change:
            return False
        
        # Update the policy
        self.selected_policies[area] = option
        return True
    
    def get_policy_summary(self):
        """Get a summary of selected policies and budget usage."""
        used_budget = self.calculate_current_usage()
        remaining_budget = self.get_remaining_budget()
        
        # Count options by type
        option_counts = {1: 0, 2: 0, 3: 0}
        for option in self.selected_policies.values():
            if option is not None:
                option_counts[option] += 1
        
        # Check if we have a mix of options (rule #4)
        has_policy_mix = len(set(self.selected_policies.values()) - {None}) > 1
        
        return {
            "used_budget": used_budget,
            "remaining_budget": remaining_budget,
            "selected_policies": self.selected_policies.copy(),
            "option_counts": option_counts,
            "has_complete_policy_set": None not in self.selected_policies.values(),
            "has_policy_mix": has_policy_mix
        }
    
    def is_valid_policy_set(self):
        """Check if the current policy set is valid according to all rules."""
        summary = self.get_policy_summary()
        
        # Rule 1: Budget limit not exceeded
        budget_valid = summary["used_budget"] <= self.total_budget
        
        # Rule 4: Policy selection variety (cannot select all from same option)
        variety_valid = summary["has_policy_mix"]
        
        # Check if all policies have been selected
        completeness_valid = summary["has_complete_policy_set"]
        
        return budget_valid and variety_valid and completeness_valid
    
    def get_feedback(self):
        """Get feedback on the current policy set."""
        summary = self.get_policy_summary()
        feedback = []
        
        # Budget feedback
        if summary["used_budget"] < self.total_budget:
            feedback.append(f"You have {summary['remaining_budget']} budget units remaining. Consider upgrading some policies.")
        elif summary["used_budget"] == self.total_budget:
            feedback.append("You have used your entire budget efficiently.")
        else:
            feedback.append("WARNING: You have exceeded your budget limit!")
        
        # Policy mix feedback
        if not summary["has_policy_mix"] and len(set(self.selected_policies.values()) - {None}) > 0:
            feedback.append("WARNING: You must choose a mix of policy options, not all from the same level.")
        
        # Completeness feedback
        if not summary["has_complete_policy_set"]:
            incomplete_areas = [area for area, option in self.selected_policies.items() if option is None]
            feedback.append(f"You still need to make decisions for: {', '.join(incomplete_areas)}")
        
        return feedback

# Example usage:
# calculator = BudgetCalculator()
# calculator.set_policy_option("Access to Education", 3)
# calculator.set_policy_option("Language Instruction", 2)
# print(calculator.get_remaining_budget())
# print(calculator.get_policy_summary())
# print(calculator.get_feedback())