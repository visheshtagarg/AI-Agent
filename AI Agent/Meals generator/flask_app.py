from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import json
import pandas as pd
import os
from pathlib import Path
import sys

# Import agents
from agents.user_interaction_agent import UserInteractionAgent
from agents.planner_agent import PlannerAgent
from agents.nutritionist_agent import NutritionistAgent
from agents.rag_retriever_agent import RAGRetrieverAgent
from agents.optimizer_agent import OptimizerAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.coach_agent import CoachAgent

app = Flask(__name__)
app.secret_key = 'smart_meal_planner_secret_key'  # For session management

# Assets paths
ASSETS_DIR = Path("static")
ICONS_DIR = ASSETS_DIR / "icons"

# Initialize agents
user_agent = UserInteractionAgent()
planner_agent = PlannerAgent()
nutritionist_agent = NutritionistAgent()
rag_agent = RAGRetrieverAgent()
optimizer_agent = OptimizerAgent()
evaluator_agent = EvaluatorAgent()
coach_agent = CoachAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    # Get form data
    user_data = {
        'name': request.form.get('name', ''),
        'age': request.form.get('age', ''),
        'gender': request.form.get('gender', ''),
        'weight': request.form.get('weight', ''),
        'height': request.form.get('height', ''),
        'activity_level': request.form.get('activity_level', ''),
        'dietary_restrictions': request.form.getlist('dietary_restrictions'),
        'health_goals': request.form.getlist('health_goals'),
        'cuisine_preferences': request.form.getlist('cuisine_preferences'),
        'allergies': request.form.get('allergies', ''),
        'budget_constraint': request.form.get('budget_constraint', 'medium'),
        'cooking_time': request.form.get('cooking_time', 'medium'),
        'cooking_skill': request.form.get('cooking_skill', 'intermediate')
    }
    
    # Process with agents
    user_profile = user_agent.process_user_input(user_data)
    meal_plan = planner_agent.generate_meal_plan(user_profile)
    nutrition_analysis = nutritionist_agent.analyze_nutrition(meal_plan)
    
    # Get recommendations
    recommendations = rag_agent.get_recommendations(user_profile)
    optimized_plan = optimizer_agent.optimize_meal_plan(meal_plan, user_profile)
    evaluation = evaluator_agent.evaluate_plan(optimized_plan, user_profile)
    coaching_tips = coach_agent.generate_coaching_tips(user_profile, optimized_plan)
    
    # Store in session for display
    session['meal_plan'] = optimized_plan
    session['nutrition_analysis'] = nutrition_analysis
    session['recommendations'] = recommendations
    session['evaluation'] = evaluation
    session['coaching_tips'] = coaching_tips
    session['user_profile'] = user_profile
    
    return redirect(url_for('meal_plan_results'))

@app.route('/meal_plan_results')
def meal_plan_results():
    # Get data from session
    meal_plan = session.get('meal_plan', {})
    nutrition_analysis = session.get('nutrition_analysis', {})
    recommendations = session.get('recommendations', [])
    evaluation = session.get('evaluation', {})
    coaching_tips = session.get('coaching_tips', [])
    user_profile = session.get('user_profile', {})
    
    return render_template(
        'results.html',
        meal_plan=meal_plan,
        nutrition_analysis=nutrition_analysis,
        recommendations=recommendations,
        evaluation=evaluation,
        coaching_tips=coaching_tips,
        user_profile=user_profile
    )

@app.route('/download_meal_plan', methods=['POST'])
def download_meal_plan():
    format_type = request.form.get('format', 'json')
    meal_plan = session.get('meal_plan', {})
    
    if format_type == 'json':
        return jsonify(meal_plan)
    elif format_type == 'csv':
        # Convert to CSV format
        # Implementation would depend on meal plan structure
        return "CSV download functionality"
    else:
        return "Unsupported format"

if __name__ == '__main__':
    app.run(debug=True)