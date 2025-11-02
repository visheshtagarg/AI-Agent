import http.server
import socketserver

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
        
        .form-section h2 {
            color: #4CAF50;
            margin-bottom: 1.5rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-row {
            display: flex;
            gap: 1rem;
        }
        
        .form-row .form-group {
            flex: 1;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
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
        }
        
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem 1.5rem;
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
                        <input type="text" id="name" name="name" required>
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
                    <h2>Lifestyle & Preferences</h2>
                    <div class="form-group">
                        <label for="activity_level">Activity Level</label>
                        <select id="activity_level" name="activity_level" required>
                            <option value="">Select</option>
                            <option value="sedentary">Sedentary (little or no exercise)</option>
                            <option value="light">Light (exercise 1-3 days/week)</option>
                            <option value="moderate">Moderate (exercise 3-5 days/week)</option>
                            <option value="active">Active (exercise 6-7 days/week)</option>
                            <option value="very_active">Very Active (intense exercise daily)</option>
                        </select>
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
                        </div>
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
        
        .day-card {
            background: #f5f5f5;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
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
            <p class="header-subtitle">Tailored to your unique needs and preferences</p>
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
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode())
        elif self.path == '/meal_plan_results':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(RESULTS_HTML.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path == '/generate_meal_plan':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Redirect to results page
            self.send_response(302)
            self.send_header('Location', '/meal_plan_results')
            self.end_headers()

# Run the server
PORT = 8000
print(f"Starting server on port {PORT}...")
print(f"Open your browser and navigate to http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), MealPlannerHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()