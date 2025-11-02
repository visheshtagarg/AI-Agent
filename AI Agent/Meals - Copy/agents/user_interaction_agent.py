import datetime


class UserInteractionAgent:
    def __init__(self):
        pass

    def parse_input(self, data: dict) -> dict:
        meals_per_day = int(data.get('meals_per_day', 4))
        meals_per_day = max(1, min(6, meals_per_day))
        
        health_cond_str = data.get('health_cond', '') or ''
        allergies_str = data.get('allergies', '') or ''
        meal_times = data.get('meal_times', [])
        if isinstance(meal_times, str):
            meal_times = [t.strip() for t in meal_times.split(';') if t.strip()]
        
        profile = {
            'age': data.get('age', 25),
            'gender': data.get('gender', 'Female'),
            'goal': data.get('goal', 'Weight maintenance'),
            'target_calories': int(data.get('target_calories', 2000)),
            'diet_pref': data.get('diet_pref', 'Vegetarian'),
            'meals_per_day': meals_per_day,
            'health_cond': [h.strip() for h in health_cond_str.split(',') if h.strip()],
            'allergies': [a.strip() for a in allergies_str.split(',') if a.strip()],
            'activity_level': data.get('activity_level', 'Medium'),
            'cuisine_preference': data.get('cuisine_preference', 'Any'),
            'meal_times': meal_times,
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        return profile

