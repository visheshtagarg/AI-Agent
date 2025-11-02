class CoachAgent:
    def __init__(self):
        pass

    def format_plan(self, plan: dict, report: dict) -> dict:
        readable = {'meals': [], 'summary': report}
        for meal, data in plan.items():
            meal_info = {
                'name': meal,
                'items': data.get('items', []),
                'calories': data.get('calories', 0),
                'meal_time': data.get('meal_time', '')
            }
            readable['meals'].append(meal_info)
        return readable

