class PlannerAgent:
    def __init__(self):
        self.default_ratios = {
            1: [1.0],
            2: [0.4, 0.6],
            3: [0.3, 0.4, 0.3],
            4: [0.25, 0.35, 0.15, 0.25],
            5: [0.2, 0.3, 0.1, 0.15, 0.25],
            6: [0.2, 0.25, 0.1, 0.1, 0.15, 0.2]
        }
        self.meal_labels = ['Breakfast', 'Lunch', 'Snack1', 'Snack2', 'Snack3', 'Dinner']
        self.default_times = {
            1: ['13:00'],
            2: ['08:00', '19:00'],
            3: ['08:00', '13:00', '19:30'],
            4: ['08:00', '13:00', '16:00', '19:30'],
            5: ['07:30', '12:30', '16:00', '19:30', '21:00'],
            6: ['08:00', '11:00', '13:00', '16:00', '19:00', '21:00']
        }

    def plan_calories(self, profile: dict) -> dict:
        n = profile.get('meals_per_day', 4)
        n = max(1, min(6, int(n)))
        ratios = self.default_ratios.get(n, self.default_ratios[4])
        target = profile['target_calories']
        
        custom_times = profile.get('meal_times', [])
        if custom_times and len(custom_times) == n:
            times = custom_times
        else:
            times = self.default_times.get(n, self.default_times[4])
        
        plan = {}
        for i, r in enumerate(ratios):
            if i < len(self.meal_labels):
                label = self.meal_labels[i]
                meal_time = times[i] if i < len(times) else times[0]
                plan[label] = {
                    'calories': int(round(target * r)),
                    'meal_time': meal_time
                }
        return plan

