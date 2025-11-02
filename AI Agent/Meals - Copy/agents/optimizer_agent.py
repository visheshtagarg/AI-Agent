class OptimizerAgent:
    def __init__(self):
        pass

    def optimize_meals(self, meals: dict, profile: dict) -> dict:
        total_target = profile['target_calories']
        total_plan = sum([m.get('calories', 0) for m in meals.values()])
        if total_plan == 0:
            return meals
        scale = total_target / total_plan
        for k in meals:
            meals[k]['calories'] = int(round(meals[k].get('calories', 0) * scale))
        return meals

