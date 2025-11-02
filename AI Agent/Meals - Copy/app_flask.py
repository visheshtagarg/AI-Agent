from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'smart_meal_planner_secret_key'

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
    
    # Store in session for display
    session['user_data'] = user_data
    
    # For demo purposes, create a simple meal plan
    meal_plan = {
        "Monday": {
            "Breakfast": {"name": "Oatmeal with Berries", "ingredients": ["Oats", "Berries", "Honey"]},
            "Lunch": {"name": "Chicken Salad", "ingredients": ["Chicken", "Lettuce", "Tomatoes"]},
            "Dinner": {"name": "Grilled Salmon", "ingredients": ["Salmon", "Asparagus", "Lemon"]}
        },
        "Tuesday": {
            "Breakfast": {"name": "Avocado Toast", "ingredients": ["Bread", "Avocado", "Eggs"]},
            "Lunch": {"name": "Quinoa Bowl", "ingredients": ["Quinoa", "Vegetables", "Tofu"]},
            "Dinner": {"name": "Pasta Primavera", "ingredients": ["Pasta", "Vegetables", "Olive Oil"]}
        }
    }
    
    session['meal_plan'] = meal_plan
    
    return redirect(url_for('meal_plan_results'))

@app.route('/meal_plan_results')
def meal_plan_results():
    # Get data from session
    meal_plan = session.get('meal_plan', {})
    user_data = session.get('user_data', {})
    
    return render_template(
        'results.html',
        meal_plan=meal_plan,
        user_profile=user_data,
        nutrition_analysis={},
        recommendations=[],
        evaluation={},
        coaching_tips=["Drink plenty of water", "Eat more vegetables"]
    )

if __name__ == '__main__':
    app.run(debug=True)