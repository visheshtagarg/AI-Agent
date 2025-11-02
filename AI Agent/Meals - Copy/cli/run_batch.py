import argparse
import csv
import json

from agents.user_interaction_agent import UserInteractionAgent
from agents.planner_agent import PlannerAgent
from agents.nutritionist_agent import NutritionistAgent
from agents.rag_retriever_agent import RAGRetrieverAgent
from agents.optimizer_agent import OptimizerAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.coach_agent import CoachAgent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--model', required=False)
    parser.add_argument('--user-id', required=False)
    parser.add_argument('--top-k', type=int, default=8)
    parser.add_argument('--retry-policy', required=False)
    args = parser.parse_args()

    user_agent = UserInteractionAgent()
    planner = PlannerAgent()
    rag = RAGRetrieverAgent()
    nutritionist = NutritionistAgent(rag_retriever=rag)
    optimizer = OptimizerAgent()
    evaluator = EvaluatorAgent()
    coach = CoachAgent()

    results = []
    with open(args.input, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            profile = user_agent.parse_input({
                'age': int(row.get('age', 25)),
                'gender': row.get('sex', 'Other'),
                'goal': row.get('goal', 'maintain'),
                'target_calories': int(float(row.get('calorie_target', 2000))),
                'diet_pref': row.get('dietary_pref', 'Vegetarian'),
                'meals_per_day': int(row.get('meal_count_preference', 4)),
                'health_cond': row.get('allergies', '')
            })
            plan = planner.plan_calories(profile)
            meals = nutritionist.generate_meals(profile, plan)
            optimized = optimizer.optimize_meals(meals, profile)
            report = evaluator.evaluate(optimized, profile)
            final_plan = coach.format_plan(optimized, report)
            results.append({'user_id': row.get('user_id', ''), 'plan': final_plan, 'evaluation': report})

    with open(args.out, 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == '__main__':
    main()

