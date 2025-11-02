def _sum_calories(plan: dict):
    return sum([v['calories'] for v in plan.values()])


class EvaluatorAgent:
    def __init__(self):
        pass

    def evaluate(self, plan: dict, profile: dict) -> dict:
        total = _sum_calories(plan)
        target = profile['target_calories']
        deviation_pct = abs(total - target) / target * 100
        diversity_score = self._diversity_score(plan)
        safety = self._safety_check(plan, profile)
        return {
            'total_calories': total,
            'target_calories': target,
            'deviation_pct': deviation_pct,
            'diversity_score': diversity_score,
            'safety': safety
        }

    def _diversity_score(self, plan):
        items = [item for meal in plan.values() for item in meal['items']]
        unique = len(set(items))
        total = len(items)
        return unique / (total + 1)

    def _safety_check(self, plan, profile):
        if profile.get('target_calories', 0) < 1000:
            return {'ok': False, 'reason': 'Target calories extremely low'}
        return {'ok': True}

