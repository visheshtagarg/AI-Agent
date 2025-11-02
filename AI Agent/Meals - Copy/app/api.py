from fastapi import FastAPI
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pydantic import BaseModel
from typing import List, Dict, Any

from agents.user_interaction_agent import UserInteractionAgent
from agents.planner_agent import PlannerAgent
from agents.nutritionist_agent import NutritionistAgent
from agents.rag_retriever_agent import RAGRetrieverAgent
from agents.optimizer_agent import OptimizerAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.coach_agent import CoachAgent


app = FastAPI(title="Diet & Calorie Recommender API")


class BatchItem(BaseModel):
    user_id: str
    age: int
    sex: str
    goal: str
    calorie_target: int | None = None
    dietary_pref: str | None = None
    allergies: str | None = None
    meal_count_preference: int | None = None


class BatchRequest(BaseModel):
    items: List[BatchItem]


@app.post("/v1/batch/run")
def run_batch(req: BatchRequest) -> Dict[str, Any]:
    user_agent = UserInteractionAgent()
    planner = PlannerAgent()
    rag = RAGRetrieverAgent()
    nutritionist = NutritionistAgent(rag_retriever=rag)
    optimizer = OptimizerAgent()
    evaluator = EvaluatorAgent()
    coach = CoachAgent()

    results = []
    for item in req.items:
        profile = user_agent.parse_input({
            'age': item.age,
            'gender': item.sex,
            'goal': item.goal,
            'target_calories': item.calorie_target or 2000,
            'diet_pref': item.dietary_pref or 'Vegetarian',
            'meals_per_day': item.meal_count_preference or 4,
            'health_cond': item.allergies or ''
        })
        plan = planner.plan_calories(profile)
        meals = nutritionist.generate_meals(profile, plan)
        optimized = optimizer.optimize_meals(meals, profile)
        report = evaluator.evaluate(optimized, profile)
        final_plan = coach.format_plan(optimized, report)
        results.append({'user_id': item.user_id, 'plan': final_plan, 'evaluation': report})
    return {"results": results}


@app.get("/v1/logs/{batch_id}")
def get_logs(batch_id: str) -> Dict[str, Any]:
    # Placeholder: real implementation would query SQLite
    return {"batch_id": batch_id, "logs": []}

