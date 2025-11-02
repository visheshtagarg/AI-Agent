import streamlit as st
import sys
import json
import pandas as pd
import os
from pathlib import Path

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    go = None
    px = None

try:
    from openpyxl import load_workbook
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

from agents.user_interaction_agent import UserInteractionAgent
from agents.planner_agent import PlannerAgent
from agents.nutritionist_agent import NutritionistAgent
from agents.rag_retriever_agent import RAGRetrieverAgent
from agents.optimizer_agent import OptimizerAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.coach_agent import CoachAgent

st.set_page_config(
    page_title='Smart AI Meal Planner',
    page_icon='🥗',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Assets paths
ASSETS_DIR = Path("assets")
BANNER_PATH = ASSETS_DIR / "banner_mealplanner.png"
LOGO_PATH = ASSETS_DIR / "logo_forkleaf.png"
BG_PATH = ASSETS_DIR / "bg_gradient.png"
ICONS_DIR = ASSETS_DIR / "icons"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(120deg, #f4fff9 0%, #eef3ff 100%);
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 0.8s ease-out;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(76, 175, 80, 0.1);
        animation: fadeIn 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
        border-color: #4CAF50;
    }
    
    .meal-card {
        background: #ffffff;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border-left: 4px solid #4CAF50;
        animation: fadeIn 0.7s ease-out;
    }
    
    .meal-card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
    }
    
    .stForm {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(103, 58, 183, 0.1);
        animation: fadeIn 0.8s ease-out;
    }
    
    button[data-testid="baseButton-primary"] {
        background: #4CAF50 !important;
        border: none !important;
        border-radius: 50px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    button[data-testid="baseButton-primary"]:hover {
        background: #45A049 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    .stDownloadButton > button {
        background: #673AB7 !important;
        border: none !important;
        border-radius: 50px !important;
        color: white !important;
    }
    
    .stDownloadButton > button:hover {
        background: #5E35B1 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(103, 58, 183, 0.3);
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        background: #ffffff;
        animation: fadeIn 0.7s ease-out;
    }
    
    .tips-section {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.1);
        animation: slideUp 0.8s ease-out;
    }
    
    .tip-item {
        background: rgba(76, 175, 80, 0.05);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        transition: all 0.3s ease;
    }
    
    .tip-item:hover {
        background: rgba(76, 175, 80, 0.1);
        transform: translateX(5px);
    }
    
    .stSuccess {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        border-radius: 12px;
    }
    
    .stError {
        background: #FFEBEE;
        border-left: 4px solid #FF5252;
        border-radius: 12px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4CAF50 !important;
        color: white !important;
    }
    
    .stProgress > div > div > div {
        background: #4CAF50 !important;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Display banner if available
if BANNER_PATH.exists():
    st.image(str(BANNER_PATH), use_container_width=True)
else:
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🥗 Smart AI Meal Planner")
    st.caption("An AI-powered multi-user diet planner with RAG + LoRA integration, interactive charts, and beautiful UI built in Streamlit.")
    st.markdown("---")
    st.markdown("### 📋 Upload or Enter User Details")
    st.markdown("### 🔄 Select Mode (Single / Batch)")
    st.markdown("### 📥 Download Output Files")
    st.markdown("---")
    st.markdown("### Project Info")
    st.info("""
    **Author:** Visheshta Garg
    
    **University:** IIT Roorkee
    
    **Degree:** B.Tech (Civil Engineering)
    """)
    st.markdown("---")
    st.markdown("**Version:** 4.0.0")
    st.markdown("---")
    st.markdown("**Built with ❤️ by Visheshta Garg, IIT Roorkee**")

tab1, tab2 = st.tabs(["👤 Single User Planner", "📂 Multi-User Planner (Batch Mode)"])

with tab1:
    # Header Section
    st.markdown('<h1 class="main-header">🥗 Smart AI Meal Planner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Generate personalized meal plans with nutrition insights and visual breakdowns.</p>', unsafe_allow_html=True)
    
    with st.form('user_form'):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input('Name', value='User')
            age = st.number_input('Age', min_value=10, max_value=90, value=25)
            gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
            goal = st.selectbox('Goal', ['Weight Loss', 'Muscle Gain', 'Maintain Weight', 'Keto', 'Low Carb', 'High Protein'])
            target_calories = st.number_input('Target Calories', min_value=800, max_value=4500, value=1800)
        with col2:
            diet_pref = st.selectbox('Diet Preference', ['Vegetarian', 'Non-Vegetarian', 'Vegan'])
            meals_per_day = st.slider('Meals Per Day', min_value=1, max_value=6, value=3)
            allergies = st.text_input('Allergies (comma separated)', '')
            health_cond = st.text_input('Health conditions (comma separated)', '')
            activity_level = st.selectbox('Activity Level', ['Low', 'Medium', 'High'])
            cuisine_pref = st.selectbox('Cuisine Preference', ['Indian', 'Continental', 'Mixed', 'Any'])
            meal_times_input = st.text_input('Meal Times (optional, semicolon-separated, e.g., 08:00;13:00;19:30)', '')
        
        submit = st.form_submit_button('🍴 Generate Meal Plan', use_container_width=True)

    if submit:
        with st.spinner('Generating your personalized meal plan...'):
            user_agent = UserInteractionAgent()
            planner = PlannerAgent()
            rag = RAGRetrieverAgent()
            if hasattr(rag, 'dependency_missing') and rag.dependency_missing:
                st.warning("RAG is disabled: missing deps in this Python environment.")
            elif hasattr(rag, 'available') and not rag.available:
                st.info("RAG installed, but storage init failed. Continuing without RAG.")
            nutritionist = NutritionistAgent(rag_retriever=rag)
            optimizer = OptimizerAgent()
            evaluator = EvaluatorAgent()
            coach = CoachAgent()

            meal_times = []
            if meal_times_input:
                meal_times = [t.strip() for t in meal_times_input.split(';') if t.strip()]

            user_profile = user_agent.parse_input({
                'age': int(age), 'gender': gender, 'goal': goal,
                'target_calories': int(target_calories), 'diet_pref': diet_pref,
                'meals_per_day': int(meals_per_day), 'health_cond': health_cond,
                'allergies': allergies, 'activity_level': activity_level,
                'cuisine_preference': cuisine_pref, 'meal_times': meal_times
            })

            calorie_plan = planner.plan_calories(user_profile)
            raw_meals = nutritionist.generate_meals(user_profile, calorie_plan)
            optimized = optimizer.optimize_meals(raw_meals, user_profile)
            report = evaluator.evaluate(optimized, user_profile)
            final_plan = coach.format_plan(optimized, report)

        st.success('✅ Meal plan generated successfully!')
        
        total_cal = sum([m.get('calories', 0) for m in final_plan.get('meals', [])])
        deviation = report.get('deviation_pct', 0)
        diversity = report.get('diversity_score', 0)
        safety_ok = report.get('safety', {}).get('ok', True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric('Total Calories', f"{total_cal} kcal", delta=f"{total_cal - user_profile['target_calories']} kcal")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric('Deviation', f"{deviation:.1f}%", delta=f"{abs(deviation):.1f}% from target", delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric('Diversity Score', f"{diversity:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric('Safety', '✅ Passed' if safety_ok else '⚠️ Review')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Output Table Section
        st.markdown('### Your Personalized Meal Plan')
        
        table_data = []
        df_plan = None
        total_cal = sum([m.get('calories', 0) for m in final_plan.get('meals', [])])
        
        for meal in final_plan.get('meals', []):
            meal_name = meal.get('name', '')
            items = '; '.join(meal.get('items', []))
            calories = meal.get('calories', 0)
            meal_time = meal.get('meal_time', '')
            # Estimate macros (simplified - in real app would come from meal data)
            carbs = int(calories * 0.45 / 4)  # grams
            protein = int(calories * 0.25 / 4)  # grams
            fat = int(calories * 0.30 / 9)  # grams
            
            table_data.append({
                'Meal': meal_name,
                'Meal_Time': meal_time,
                'Items': items,
                'Calories': calories,
                'Carbs': carbs,
                'Protein': protein,
                'Fat': fat
            })
        
        if table_data:
            df_plan = pd.DataFrame(table_data)
            st.dataframe(
                df_plan,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Calories": st.column_config.NumberColumn("Calories", format="%d kcal"),
                    "Carbs": st.column_config.NumberColumn("Carbs", format="%d g"),
                    "Protein": st.column_config.NumberColumn("Protein", format="%d g"),
                    "Fat": st.column_config.NumberColumn("Fat", format="%d g")
                }
            )
        else:
            st.info("No meal plan generated.")
        
        # Charts Section
        st.markdown('### Visualizations')
        if PLOTLY_AVAILABLE and table_data:
            col1, col2 = st.columns(2)
            
            with col1:
                # Macronutrient Distribution (Donut Chart)
                st.markdown('#### Macronutrient Distribution')
                carbs_cal = int(total_cal * 0.45)
                protein_cal = int(total_cal * 0.25)
                fat_cal = int(total_cal * 0.30)
                
                fig_donut = go.Figure(data=[go.Pie(
                    labels=['Carbohydrates', 'Proteins', 'Fats'],
                    values=[carbs_cal, protein_cal, fat_cal],
                    hole=0.6,
                    marker_colors=['#66BB6A', '#42A5F5', '#FF7043'],
                    textinfo='label+percent',
                    textposition='inside'
                )])
                fig_donut.update_layout(
                    showlegend=True,
                    height=300,
                    font=dict(family="Poppins", size=12),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    transition={'duration': 500, 'easing': 'cubic-in-out'}
                )
                st.plotly_chart(fig_donut, use_container_width=True)
                
                # Calorie Split by Meal (Pie Chart)
                st.markdown('#### Calorie Split by Meal')
                meal_names = [m.get('name', '') for m in final_plan.get('meals', [])]
                meal_calories = [m.get('calories', 0) for m in final_plan.get('meals', [])]
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=meal_names,
                    values=meal_calories,
                    hole=0.4,
                    marker_colors=['#66BB6A', '#42A5F5', '#FF7043', '#FFD54F', '#AB47BC', '#66BB6A'],
                    textinfo='label+percent',
                    textposition='outside'
                )])
                fig_pie.update_layout(
                    showlegend=True,
                    height=300,
                    font=dict(family="Poppins", size=12),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    transition={'duration': 500, 'easing': 'cubic-in-out'}
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Daily Nutrient Intake (Bar Chart)
                st.markdown('#### Daily Nutrient Intake')
                nutrient_data = {
                    'Fiber': int(total_cal * 0.02),
                    'Sugar': int(total_cal * 0.05),
                    'Vitamins': int(total_cal * 0.01),
                    'Minerals': int(total_cal * 0.01)
                }
                nutrient_df = pd.DataFrame([nutrient_data])
                
                fig_bar = go.Figure(data=[
                    go.Bar(
                        x=list(nutrient_data.keys()),
                        y=list(nutrient_data.values()),
                        marker_color=['#66BB6A', '#42A5F5', '#FF7043', '#FFD54F']
                    )
                ])
                fig_bar.update_layout(
                    height=300,
                    font=dict(family="Poppins", size=12),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    transition={'duration': 500, 'easing': 'cubic-in-out'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Install plotly for charts: pip install plotly")
        
        # Tips Section
        st.markdown("---")
        st.markdown('<div class="tips-section">', unsafe_allow_html=True)
        st.markdown('### 💡 Health & Nutrition Tips')
        
        health_tips = [
            "Start your day with a high-protein breakfast.",
            "Avoid skipping meals; it slows down metabolism.",
            "Drink 2.5L of water daily.",
            "Include at least 1 serving of fruits every day.",
            "Replace sugar drinks with fresh juices or smoothies."
        ]
        
        for tip in health_tips:
            st.markdown(f'<div class="tip-item">💡 {tip}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Section
        st.markdown("---")
        st.markdown('### 📥 Export Options')
        if df_plan is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                csv_data = df_plan.to_csv(index=False)
                st.download_button(
                    '📥 Download Plan (CSV)',
                    csv_data,
                    'outputs/single_user_plan.csv',
                    'text/csv',
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    '📥 Download Plan (JSON)',
                    json.dumps(final_plan, indent=2),
                    'single_user_plan.json',
                    'application/json',
                    use_container_width=True
                )
            with col3:
                st.info("📄 PDF export coming soon")
        else:
            st.info("Generate a meal plan to enable downloads.")
        
        with st.expander('📋 View Detailed Plan & Metrics'):
            st.json(final_plan)
            st.json(report)

with tab2:
    # Header Section
    st.markdown('<h1 class="main-header">Multi-User Meal Planning</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Upload a CSV file to generate meal plans for multiple people at once.</p>', unsafe_allow_html=True)
    
    # Upload Section
    st.markdown('### Upload User Profile Sheet')
    uploaded_file = st.file_uploader('Upload CSV or Excel file', type=['csv', 'xlsx'], help='Accepted formats: CSV or Excel (.xlsx)')
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                if not EXCEL_AVAILABLE:
                    st.error("Excel support requires openpyxl. Install with: pip install openpyxl")
                    st.stop()
                df = pd.read_excel(uploaded_file, sheet_name='Users', engine='openpyxl')
            else:
                df = pd.read_csv(uploaded_file)
            file_type = "Excel" if uploaded_file.name.endswith('.xlsx') else "CSV"
            st.success(f'✅ Loaded {len(df)} users from {file_type}')
            
            with st.expander('Preview Input Data'):
                st.dataframe(df.head(10), use_container_width=True)
            
            if st.button('🚀 Generate Meal Plans for All Users', type='primary', use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                all_results = []
                errors = []
                
                user_agent = UserInteractionAgent()
                planner = PlannerAgent()
                rag = RAGRetrieverAgent()
                nutritionist = NutritionistAgent(rag_retriever=rag)
                optimizer = OptimizerAgent()
                evaluator = EvaluatorAgent()
                coach = CoachAgent()
                
                for idx, row in df.iterrows():
                    try:
                        status_text.text(f'Processing {idx + 1}/{len(df)}: {row.get("Name", "Unknown")}')
                        progress_bar.progress((idx + 1) / len(df))
                        
                        name = str(row.get('Name', f'User_{idx+1}'))
                        user_id = str(row.get('UserID', f'user_{idx+1:03d}'))
                        age = int(row.get('Age', 25))
                        gender = str(row.get('Gender', 'Other')).strip()
                        goal = str(row.get('Goal', 'Maintenance')).strip()
                        target_cal = row.get('Target_Calories', None)
                        if pd.isna(target_cal):
                            target_cal = 2000
                        target_cal = int(target_cal)
                        diet_pref = str(row.get('Diet_Preference', 'Vegetarian')).strip()
                        meals_per_day = int(row.get('Meals_Per_Day', 4))
                        meals_per_day = max(1, min(6, meals_per_day))
                        allergies = str(row.get('Allergies', ''))
                        health_cond = str(row.get('Health_Conditions', ''))
                        activity_level = str(row.get('Activity_Level', 'Medium'))
                        cuisine_pref = str(row.get('Cuisine_Preference', 'Any'))
                        meal_times_str = str(row.get('Meal_Times', ''))
                        meal_times = [t.strip() for t in meal_times_str.split(';') if t.strip()] if meal_times_str else []
                        
                        if meals_per_day < 1 or meals_per_day > 6:
                            errors.append({'Row': idx + 1, 'Name': name, 'Error': f'Invalid Meals_Per_Day: {meals_per_day} (must be 1-6)'})
                            continue
                        if target_cal < 800 or target_cal > 4500:
                            errors.append({'Row': idx + 1, 'Name': name, 'Error': f'Invalid Target_Calories: {target_cal} (must be 800-4500)'})
                            continue
                        if meal_times and len(meal_times) != meals_per_day:
                            errors.append({'Row': idx + 1, 'Name': name, 'Error': f'Meal_Times count ({len(meal_times)}) must match Meals_Per_Day ({meals_per_day})'})
                            continue
                        if gender not in ['Male', 'Female', 'Other']:
                            errors.append({'Row': idx + 1, 'Name': name, 'Error': f'Invalid Gender: {gender}'})
                            continue
                        
                        profile = user_agent.parse_input({
                            'age': age, 'gender': gender, 'goal': goal,
                            'target_calories': target_cal, 'diet_pref': diet_pref,
                            'meals_per_day': meals_per_day, 'health_cond': health_cond,
                            'allergies': allergies, 'activity_level': activity_level,
                            'cuisine_preference': cuisine_pref, 'meal_times': meal_times
                        })
                        
                        plan = planner.plan_calories(profile)
                        meals = nutritionist.generate_meals(profile, plan)
                        optimized = optimizer.optimize_meals(meals, profile)
                        report = evaluator.evaluate(optimized, profile)
                        final_plan = coach.format_plan(optimized, report)
                        
                        total_cal = sum([m.get('calories', 0) for m in final_plan.get('meals', [])])
                        
                        for meal in final_plan.get('meals', []):
                            all_results.append({
                                'UserID': user_id,
                                'Name': name,
                                'Goal': goal,
                                'Meals_Per_Day': meals_per_day,
                                'Meal': meal.get('name', ''),
                                'Meal_Time': meal.get('meal_time', ''),
                                'Items': '; '.join(meal.get('items', [])),
                                'Meal_Calories': meal.get('calories', 0),
                                'Total_Calories': total_cal,
                                'Target_Calories': target_cal,
                                'Calorie_Deviation_%': report.get('deviation_pct', 0)
                            })
                    
                    except Exception as e:
                        errors.append({'Row': idx + 1, 'Name': row.get('Name', 'Unknown'), 'Error': str(e)})
                
                progress_bar.empty()
                status_text.empty()
                
                if all_results:
                    st.success(f'✅ Successfully processed {len(df) - len(errors)}/{len(df)} users!')
                    
                    results_df = pd.DataFrame(all_results)
                    
                    # Output Table Section
                    st.markdown('### Generated Plans Summary')
                    summary_df = results_df.groupby('UserID').agg({
                        'Name': 'first',
                        'Goal': 'first',
                        'Meals_Per_Day': 'first',
                        'Total_Calories': 'first',
                        'Calorie_Deviation_%': 'first'
                    }).reset_index()
                    summary_df = summary_df.rename(columns={'Calorie_Deviation_%': 'Deviation(%)'})
                    
                    st.dataframe(
                        summary_df[['UserID', 'Name', 'Goal', 'Meals_Per_Day', 'Total_Calories', 'Deviation(%)']],
                        use_container_width=True,
                        height=400,
                        column_config={
                            "Deviation(%)": st.column_config.NumberColumn(
                                "Deviation(%)",
                                format="%.1f%%",
                                help="Deviation from target calories"
                            ),
                            "Total_Calories": st.column_config.NumberColumn(
                                "Total_Calories",
                                format="%d kcal"
                            )
                        }
                    )
                    
                    # Charts Section
                    st.markdown('### Visualizations')
                    if PLOTLY_AVAILABLE and len(summary_df) > 0:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Calorie Comparison per User (Stacked Bar)
                            st.markdown('#### Calorie Comparison per User')
                            # Get target calories from results
                            target_cals = results_df.groupby('UserID')['Target_Calories'].first().reset_index()
                            target_map = dict(zip(target_cals['UserID'], target_cals['Target_Calories']))
                            summary_df['Target'] = summary_df['UserID'].map(target_map)
                            
                            fig_stacked = go.Figure()
                            fig_stacked.add_trace(go.Bar(
                                name='Target',
                                x=summary_df['Name'],
                                y=summary_df['Target'],
                                marker_color='#66BB6A'
                            ))
                            fig_stacked.add_trace(go.Bar(
                                name='Actual',
                                x=summary_df['Name'],
                                y=summary_df['Total_Calories'],
                                marker_color='#42A5F5'
                            ))
                            fig_stacked.update_layout(
                                barmode='group',
                                height=300,
                                font=dict(family="Poppins", size=12),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                transition={'duration': 500, 'easing': 'cubic-in-out'}
                            )
                            st.plotly_chart(fig_stacked, use_container_width=True)
                        
                        with col2:
                            # Macro Balance per User (Heatmap-like Stacked Bar)
                            st.markdown('#### Macro Balance per User')
                            # Estimate macros
                            summary_df['Protein_Cal'] = summary_df['Total_Calories'] * 0.25
                            summary_df['Carbs_Cal'] = summary_df['Total_Calories'] * 0.45
                            summary_df['Fat_Cal'] = summary_df['Total_Calories'] * 0.30
                            
                            fig_heatmap = go.Figure()
                            fig_heatmap.add_trace(go.Bar(
                                name='Protein',
                                x=summary_df['Name'],
                                y=summary_df['Protein_Cal'],
                                marker_color='#42A5F5'
                            ))
                            fig_heatmap.add_trace(go.Bar(
                                name='Carbs',
                                x=summary_df['Name'],
                                y=summary_df['Carbs_Cal'],
                                marker_color='#66BB6A'
                            ))
                            fig_heatmap.add_trace(go.Bar(
                                name='Fat',
                                x=summary_df['Name'],
                                y=summary_df['Fat_Cal'],
                                marker_color='#FF7043'
                            ))
                            fig_heatmap.update_layout(
                                barmode='stack',
                                height=300,
                                font=dict(family="Poppins", size=12),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                transition={'duration': 500, 'easing': 'cubic-in-out'}
                            )
                            st.plotly_chart(fig_heatmap, use_container_width=True)
                    
                    # Tips Section
                    st.markdown("---")
                    st.markdown('<div class="tips-section">', unsafe_allow_html=True)
                    st.markdown('### 🏋️ Batch Insights')
                    
                    batch_tips = [
                        "Users with >15% deviation may need calorie goal adjustment.",
                        "Highlight users low in protein for muscle-oriented plans.",
                        "Encourage consistent meal timing for metabolic stability."
                    ]
                    
                    for tip in batch_tips:
                        st.markdown(f'<div class="tip-item">💡 {tip}</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download Section
                    st.markdown("---")
                    st.markdown('### Export Batch Results')
                    col1, col2 = st.columns(2)
                    with col1:
                        # Excel export
                        from io import BytesIO
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            results_df.to_excel(writer, index=False, sheet_name='Meal Plans')
                        excel_data = output.getvalue()
                        st.download_button(
                            '📥 Download Results (Excel)',
                            excel_data,
                            'outputs/multi_user_plan.xlsx',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            use_container_width=True
                        )
                    with col2:
                        csv_output = results_df.to_csv(index=False)
                        st.download_button(
                            '📥 Download Results (CSV)',
                            csv_output,
                            'outputs/multi_user_plan.csv',
                            'text/csv',
                            use_container_width=True
                        )
                
                if errors:
                    st.error(f'❌ {len(errors)} errors encountered:')
                    errors_df = pd.DataFrame(errors)
                    st.dataframe(errors_df, use_container_width=True)
        
        except Exception as e:
            st.error(f'Error reading CSV file: {str(e)}')
