class BudgetOptimizer:

    @staticmethod
    def optimize_budget(
        guest_count,
        budget
    ):

        minimum_budget = guest_count * 500

        if budget < minimum_budget:

            return {
                "feasible": False,
                "suggested_budget": minimum_budget
            }

        return {
            "feasible": True,
            "suggested_budget": budget
        }