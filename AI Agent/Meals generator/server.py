import http.server
import socketserver
import urllib.parse

# HTML templates
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart AI Meal Planner</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }
        
        body {
            background: linear-gradient(120deg, #f4fff9 0%, #eef3ff 100%);
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        
        header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #4CAF50;
            margin-bottom: 0.5rem;
        }
        
        .header-subtitle {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 2rem;
        }
        
        .form-container {
            background: #ffffff;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .form-section {
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
        }
        
        .form-row .form-group {
            flex: 1 1 200px;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #555;
        }
        
        input[type="text"],
        input[type="number"],
        select,
        textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus,
        select:focus,
        textarea:focus {
            border-color: #4CAF50;
            outline: none;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
        
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 0.5rem;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        
        .checkbox-label input {
            margin-right: 0.5rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: #4CAF50;
            color: white;
        }
        
        .btn-primary:hover {
            background: #45A049;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        }
        
        footer {
            text-align: center;
            padding: 2rem 0;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="main-header">Smart AI Meal Planner</h1>
            <p class="header-subtitle">Personalized nutrition plans powered by AI</p>
        </header>

        <div class="form-container">
            <form action="/generate_meal_plan" method="post" class="meal-form">
                <div class="form-section">
                    <h2>Personal Information</h2>
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" id="name" name="name" placeholder="Enter your name" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="age">Age</label>
                            <input type="number" id="age" name="age" min="1" max="120" required>
                        </div>
                        <div class="form-group">
                            <label for="gender">Gender</label>
                            <select id="gender" name="gender" required>
                                <option value="">Select</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="form-section">
                    <h2>Health & Nutrition</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="height">Height (cm)</label>
                            <input type="number" id="height" name="height" min="50" max="250" required>
                        </div>
                        <div class="form-group">
                            <label for="weight">Weight (kg)</label>
                            <input type="number" id="weight" name="weight" min="20" max="300" required>
                        </div>
                        <div class="form-group">
                            <label for="activity_level">Activity Level</label>
                            <select id="activity_level" name="activity_level" required>
                                <option value="">Select</option>
                                <option value="sedentary">Sedentary</option>
                                <option value="light">Light Activity</option>
                                <option value="moderate">Moderate Activity</option>
                                <option value="high">High Activity</option>
                                <option value="very_high">Very High Activity</option>
                                <option value="light">Light Activity</option>
                                <option value="moderate">Moderate Activity</option>
                                <option value="high">High Activity</option>
                                <option value="very_high">Very High Activity</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Health Goals</label>
                        <div class="checkbox-group">
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="weight_loss">
                                Weight Loss
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="muscle_gain">
                                Muscle Gain
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="maintenance">
                                Maintenance
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="heart_health">
                                Heart Health
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="diabetes_management">
                                Diabetes Management
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="energy_boost">
                                Energy Boost
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="gut_health">
                                Gut Health
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="immune_support">
                                Immune Support
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" name="health_goals" value="anti_inflammatory">
                                Anti-Inflammatory
                            </label>
                        </div>
                    </div>
                </div>
                
                <div class="form-section">
                    <h2>Meal Plan Preferences</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="days">Number of Days</label>
                            <select id="days" name="days" required>
                                <option value="1">1 Day</option>
                                <option value="3" selected>3 Days</option>
                                <option value="7">7 Days</option>
                                <option value="14">14 Days</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="food_type">Food Type</label>
                            <select id="food_type" name="food_type">
                                <option value="all">All Foods</option>
                                <option value="vegetarian">Vegetarian</option>
                                <option value="vegan">Vegan</option>
                                <option value="pescatarian">Pescatarian</option>
                                <option value="keto">Keto</option>
                                <option value="paleo">Paleo</option>
                                <option value="gluten_free">Gluten-Free</option>
                                <option value="low_carb">Low Carb</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="cuisine_type">Cuisine Type</label>
                        <select id="cuisine_type" name="cuisine_type">
                            <option value="any">Any Cuisine</option>
                            <option value="indian">Indian</option>
                            <option value="italian">Italian</option>
                            <option value="mexican">Mexican</option>
                            <option value="chinese">Chinese</option>
                            <option value="japanese">Japanese</option>
                            <option value="mediterranean">Mediterranean</option>
                            <option value="thai">Thai</option>
                            <option value="american">American</option>
                            <option value="french">French</option>
                            <option value="middle_eastern">Middle Eastern</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="allergies">Allergies or Foods to Avoid</label>
                        <input type="text" id="allergies" name="allergies" placeholder="e.g., nuts, dairy, shellfish">
                    </div>
                </div>

                <div class="form-actions" style="text-align: center; margin-top: 2rem;">
                    <button type="submit" class="btn btn-primary">Generate Meal Plan</button>
                </div>
            </form>
        </div>
    </div>

    <footer>
        <p>&copy; 2023 Smart AI Meal Planner. All rights reserved.</p>
    </footer>
</body>
</html>
"""

RESULTS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Meal Plan - Smart AI Meal Planner</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }
        
        body {
            background: linear-gradient(120deg, #f4fff9 0%, #eef3ff 100%);
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        
        header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #4CAF50;
            margin-bottom: 0.5rem;
        }
        
        .header-subtitle {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 2rem;
        }
        
        .results-container {
            background: #ffffff;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .user-profile-summary,
        .meal-plan-section {
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }
        
        .health-tips-section {
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }
        
        .tips-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }
        
        .tip-card {
            background: #f9fff9;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .tip-card h3 {
            color: #4CAF50;
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }
        
        h2 {
            color: #4CAF50;
            margin-bottom: 1.5rem;
        }
        
        .profile-details {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        .profile-item {
            display: flex;
            flex-direction: column;
        }
        
        .label {
            font-weight: 600;
            color: #666;
            font-size: 0.9rem;
        }
        
        .value {
            font-size: 1.1rem;
        }
        
        /* Horizontal layout for days */
        .days-container {
            display: flex;
            flex-wrap: nowrap;
            overflow-x: auto;
            gap: 1.5rem;
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .day-card {
            background: #f5f5f5;
            border-radius: 12px;
            padding: 1.5rem;
            min-width: 300px;
            flex: 0 0 auto;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .day-card h3 {
            color: #4CAF50;
            margin-bottom: 1rem;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 0.5rem;
        }
        
        .meal-card {
            background: #ffffff;
            padding: 1.2rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #4CAF50;
        }
        
        .meal-card h4 {
            color: #4CAF50;
            margin-bottom: 0.5rem;
        }
        
        .meal-name {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .meal-ingredients {
            margin-top: 1rem;
        }
        
        .meal-ingredients h5 {
            margin-bottom: 0.5rem;
        }
        
        .meal-ingredients ul {
            padding-left: 1.5rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-block;
            text-decoration: none;
            text-align: center;
        }
        
        .btn-primary {
            background: #4CAF50;
            color: white;
        }
        
        .btn-primary:hover {
            background: #45A049;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        }
        
        .actions {
            text-align: center;
            margin-top: 2rem;
        }
        
        footer {
            text-align: center;
            padding: 2rem 0;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="main-header">Your Personalized Meal Plan</h1>
            <p class="plan-description">Here's your custom meal plan based on your preferences</p>
        </header>

        <div class="results-container">
            <div class="user-profile-summary">
                <h2>Profile Summary</h2>
                <div class="profile-details">
                    <div class="profile-item">
                        <span class="label">Name:</span>
                        <span class="value">John Doe</span>
                    </div>
                    <div class="profile-item">
                        <span class="label">Age:</span>
                        <span class="value">35</span>
                    </div>
                    <div class="profile-item">
                        <span class="label">Gender:</span>
                        <span class="value">Male</span>
                    </div>
                    <div class="profile-item">
                        <span class="label">Activity Level:</span>
                        <span class="value">Moderate</span>
                    </div>
                </div>
            </div>

            <div class="meal-plan-section">
                <h2>7-Day Meal Plan</h2>
                
                <div class="days-container">
                    <div class="day-card">
                        <h3>Monday</h3>
                        
                        <div class="meal-card">
                            <h4>Breakfast</h4>
                            <div class="meal-name">Oatmeal with Berries</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>1/2 cup rolled oats</li>
                                    <li>1 cup almond milk</li>
                                    <li>1/4 cup mixed berries</li>
                                    <li>1 tbsp honey</li>
                                    <li>1 tbsp chia seeds</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Lunch</h4>
                            <div class="meal-name">Grilled Chicken Salad</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>4 oz grilled chicken breast</li>
                                    <li>2 cups mixed greens</li>
                                    <li>1/4 cup cherry tomatoes</li>
                                    <li>1/4 cucumber, sliced</li>
                                    <li>2 tbsp olive oil and lemon dressing</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Dinner</h4>
                            <div class="meal-name">Baked Salmon with Vegetables</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>5 oz salmon fillet</li>
                                    <li>1 cup roasted asparagus</li>
                                    <li>1/2 cup quinoa</li>
                                    <li>1 tbsp olive oil</li>
                                    <li>Lemon and herbs to taste</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="day-card">
                        <h3>Tuesday</h3>
                        
                        <div class="meal-card">
                            <h4>Breakfast</h4>
                            <div class="meal-name">Avocado Toast with Eggs</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>2 slices whole grain bread</li>
                                    <li>1/2 avocado, mashed</li>
                                    <li>2 eggs, poached</li>
                                    <li>Salt, pepper, and red pepper flakes to taste</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Lunch</h4>
                            <div class="meal-name">Quinoa Buddha Bowl</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>1/2 cup cooked quinoa</li>
                                    <li>1/4 cup roasted chickpeas</li>
                                    <li>1/4 cup roasted sweet potatoes</li>
                                    <li>1/4 avocado, sliced</li>
                                    <li>1 cup mixed greens</li>
                                    <li>2 tbsp tahini dressing</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Dinner</h4>
                            <div class="meal-name">Turkey Meatballs with Zucchini Noodles</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>4 oz turkey meatballs</li>
                                    <li>2 cups zucchini noodles</li>
                                    <li>1/2 cup marinara sauce</li>
                                    <li>1 tbsp grated parmesan</li>
                                    <li>Fresh basil for garnish</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="day-card">
                        <h3>Wednesday</h3>
                        
                        <div class="meal-card">
                            <h4>Breakfast</h4>
                            <div class="meal-name">Greek Yogurt Parfait</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>1 cup Greek yogurt</li>
                                    <li>1/4 cup granola</li>
                                    <li>1/4 cup mixed berries</li>
                                    <li>1 tbsp honey</li>
                                    <li>1 tbsp chopped nuts</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Lunch</h4>
                            <div class="meal-name">Mediterranean Wrap</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>1 whole grain wrap</li>
                                    <li>2 tbsp hummus</li>
                                    <li>1/4 cup cucumber, sliced</li>
                                    <li>1/4 cup cherry tomatoes, halved</li>
                                    <li>2 oz grilled chicken</li>
                                    <li>1 tbsp feta cheese</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Dinner</h4>
                            <div class="meal-name">Vegetable Stir Fry with Tofu</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>4 oz firm tofu, cubed</li>
                                    <li>2 cups mixed vegetables</li>
                                    <li>1/2 cup brown rice</li>
                                    <li>2 tbsp low-sodium soy sauce</li>
                                    <li>1 tsp sesame oil</li>
                                    <li>1 clove garlic, minced</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="day-card">
                        <h3>Thursday</h3>
                        
                        <div class="meal-card">
                            <h4>Breakfast</h4>
                            <div class="meal-name">Spinach and Mushroom Omelette</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>2 eggs</li>
                                    <li>1/2 cup spinach</li>
                                    <li>1/4 cup mushrooms, sliced</li>
                                    <li>1 tbsp feta cheese</li>
                                    <li>Salt and pepper to taste</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Lunch</h4>
                            <div class="meal-name">Lentil Soup with Whole Grain Bread</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>1 cup lentil soup</li>
                                    <li>1 slice whole grain bread</li>
                                    <li>1 tsp olive oil</li>
                                    <li>Fresh herbs for garnish</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Dinner</h4>
                            <div class="meal-name">Grilled Steak with Sweet Potato</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>4 oz lean steak</li>
                                    <li>1 medium sweet potato, baked</li>
                                    <li>1 cup steamed broccoli</li>
                                    <li>1 tbsp olive oil</li>
                                    <li>Herbs and spices to taste</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="day-card">
                        <h3>Friday</h3>
                        
                        <div class="meal-card">
                            <h4>Breakfast</h4>
                            <div class="meal-name">Smoothie Bowl</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>1 frozen banana</li>
                                    <li>1/2 cup frozen berries</li>
                                    <li>1/2 cup almond milk</li>
                                    <li>1 tbsp almond butter</li>
                                    <li>Toppings: granola, coconut flakes, chia seeds</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Lunch</h4>
                            <div class="meal-name">Tuna Salad Sandwich</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>3 oz canned tuna in water</li>
                                    <li>1 tbsp Greek yogurt</li>
                                    <li>1 tbsp diced celery</li>
                                    <li>2 slices whole grain bread</li>
                                    <li>Lettuce and tomato</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="meal-card">
                            <h4>Dinner</h4>
                            <div class="meal-name">Vegetable and Chickpea Curry</div>
                            
                            <div class="meal-ingredients">
                                <h5>Ingredients:</h5>
                                <ul>
                                    <li>1/2 cup chickpeas</li>
                                    <li>1 cup mixed vegetables</li>
                                    <li>1/4 cup coconut milk</li>
                                    <li>1 tbsp curry powder</li>
                                    <li>1/2 cup brown rice</li>
                                    <li>Fresh cilantro for garnish</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="health-tips-section">
            <h2>Health Tips</h2>
            <div class="tips-container">
                <div class="tip-card">
                    <h3>Stay Hydrated</h3>
                    <p>Drink at least 8 glasses of water daily to maintain proper hydration and support metabolism.</p>
                </div>
                <div class="tip-card">
                    <h3>Portion Control</h3>
                    <p>Use smaller plates and be mindful of portion sizes to avoid overeating.</p>
                </div>
                <div class="tip-card">
                    <h3>Regular Exercise</h3>
                    <p>Aim for at least 30 minutes of moderate exercise most days of the week.</p>
                </div>
                <div class="tip-card">
                    <h3>Mindful Eating</h3>
                    <p>Eat slowly and without distractions to better recognize your body's hunger signals.</p>
                </div>
            </div>
        </div>

        <div class="actions">
            <a href="/" class="btn btn-primary">Create New Plan</a>
        </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2023 Smart AI Meal Planner. All rights reserved.</p>
    </footer>
</body>
</html>
"""

# Simple HTTP server
class MealPlannerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"GET request for: {self.path}")
        path = self.path.split('?')[0]
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode())
        elif path == '/meal_plan_results':
            # Parse query parameters to get user details
            query_components = {}
            if '?' in self.path:
                query = self.path.split('?')[1]
                query_components = dict(qc.split('=') for qc in query.split('&') if '=' in qc)
            
            # Get user details from query parameters or use defaults
            user_name = urllib.parse.unquote(query_components.get('name', 'User'))
            if not user_name or user_name.strip() == '':
                user_name = 'User'
                
            age = urllib.parse.unquote(query_components.get('age', '35'))
            gender = urllib.parse.unquote(query_components.get('gender', 'Not specified'))
            activity_level = urllib.parse.unquote(query_components.get('activity_level', 'Moderate'))
            
            # Replace placeholder in results HTML with actual user name
            custom_results_html = RESULTS_HTML.replace('<h1 class="main-header">Your Personalized Meal Plan</h1>', f'<h1 class="main-header">{user_name}\'s Personalized Meal Plan</h1>')
            
            # Update all profile details
            custom_results_html = custom_results_html.replace('<span class="value">John Doe</span>', f'<span class="value">{user_name}</span>')
            custom_results_html = custom_results_html.replace('<span class="value">35</span>', f'<span class="value">{age}</span>')
            custom_results_html = custom_results_html.replace('<span class="value">Male</span>', f'<span class="value">{gender}</span>')
            custom_results_html = custom_results_html.replace('<span class="value">Moderate</span>', f'<span class="value">{activity_level}</span>')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(custom_results_html.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path == '/generate_meal_plan':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_params = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            # Store user data in a cookie or session
            user_name = post_params.get('name', ['User'])[0]
            if not user_name or user_name.strip() == '':
                user_name = 'User'
                
            # Get additional profile details
            age = post_params.get('age', ['35'])[0]
            gender = post_params.get('gender', ['Not specified'])[0]
            activity_level = post_params.get('activity_level', ['Moderate'])[0]
                
            # Redirect to results page with all user details
            self.send_response(302)
            self.send_header('Location', f'/meal_plan_results?name={urllib.parse.quote(user_name)}&age={urllib.parse.quote(age)}&gender={urllib.parse.quote(gender)}&activity_level={urllib.parse.quote(activity_level)}')
            self.end_headers()

# Run the server
PORT = 8080
print(f"Server running at http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), MealPlannerHandler) as httpd:
    httpd.serve_forever()