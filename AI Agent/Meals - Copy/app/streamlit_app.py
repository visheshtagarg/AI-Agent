import streamlit as st
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import json
from io import BytesIO

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


st.set_page_config(page_title='Smart Meal Planner (RAG + LoRA)', page_icon='🥗', layout='wide')
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #7C4DFF;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)
st.title('🥗 Smart Meal Planner — Batch Mode')

tab1, tab2 = st.tabs(["📋 CSV Format Guide", "🚀 Batch Processing"])

with tab1:
    st.subheader('CSV Format Requirements')
    st.markdown("""
    **Upload a CSV file with the following columns (case-insensitive):**
    
    ### Required Columns:
    - **UserID** (string): Unique user identifier
    - **Name** (string): User's name
    - **Age** (int): 10-100
    - **Gender** (string): Male / Female / Other
    - **Goal** (string): Weight loss, Weight maintenance, Muscle gain, Fat loss, Balanced diet, Keto, Low-carb, High-protein, Diabetic-friendly, Heart-healthy, Pescatarian, Gluten-free
    - **Target_Calories** (int): 800-4500
    - **Diet_Preference** (string): Vegetarian / Non-vegetarian / Vegan / Pescatarian
    - **Meals_Per_Day** (int): 1-6 (will be clipped if outside range)
    - **Allergies** (string): Comma-separated allergies
    - **Health_Conditions** (string): Comma-separated health conditions
    - **Meal_Times** (string): Semicolon-separated times (HH:MM format)
    
    ### Optional Columns:
    - **Activity_Level** (string): Low / Medium / High
    - **Cuisine_Preference** (string): Indian / Continental / Mixed / Any
    
    ### Validation Rules:
    - Meals_Per_Day must be between 1 and 6
    - Target_Calories must be between 800 and 4500
    - Meal_Times count must match Meals_Per_Day
    - Gender must be Male, Female, or Other
    
    ### Example CSV:
    """)
    
    example_data = {
        'UserID': ['U001', 'U002', 'U003'],
        'Name': ['Aarav', 'Visheshta', 'Priya'],
        'Age': [25, 22, 30],
        'Gender': ['Male', 'Female', 'Female'],
        'Goal': ['Muscle gain', 'Weight loss', 'Balanced diet'],
        'Target_Calories': [2800, 1800, 2000],
        'Diet_Preference': ['Non-vegetarian', 'Vegetarian', 'Vegan'],
        'Meals_Per_Day': [5, 4, 3],
        'Allergies': ['None', 'None', 'Peanuts'],
        'Health_Conditions': ['None', 'Low sugar', 'None'],
        'Meal_Times': ['07:00;11:30;15:30;19:00;21:30', '08:00;13:00;19:00', '08:00;13:00;19:30'],
        'Activity_Level': ['High', 'Medium', 'Low'],
        'Cuisine_Preference': ['Indian', 'Continental', 'Indian']
    }
    example_df = pd.DataFrame(example_data)
    st.dataframe(example_df, use_container_width=True, hide_index=True)
    
    csv_string = example_df.to_csv(index=False)
    st.download_button(
        '📥 Download Example CSV Template',
        csv_string,
        'example_batch_input.csv',
        'text/csv',
        key='download-template'
    )

with tab2:
    st.subheader('Batch CSV Processing')
    csv_file = st.file_uploader('Upload CSV file with user data', type=['csv'])
    
    if csv_file:
        try:
            df = pd.read_csv(csv_file)
            st.success(f'✅ Loaded {len(df)} users from CSV')
            
            st.subheader('📊 Preview Input Data')
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
                        status_text.text(f'Processing user {idx + 1}/{len(df)}: {row.get("Name", "Unknown")}')
                        progress_bar.progress((idx + 1) / len(df))
                        
                        name = str(row.get('Name', f'User_{idx+1}'))
                        age = int(row.get('Age', 25))
                        gender = str(row.get('Gender', 'Other')).strip()
                        goal = str(row.get('Goal', 'Maintain weight')).strip()
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
                        
                        profile = user_agent.parse_input({
                            'age': age,
                            'gender': gender,
                            'goal': goal,
                            'target_calories': target_cal,
                            'diet_pref': diet_pref,
                            'meals_per_day': meals_per_day,
                            'health_cond': health_cond,
                            'allergies': allergies,
                            'activity_level': activity_level,
                            'cuisine_preference': cuisine_pref,
                            'meal_times': meal_times
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
                        errors.append({
                            'Row': idx + 1,
                            'Name': row.get('Name', 'Unknown'),
                            'Error': str(e)
                        })
                
                progress_bar.empty()
                status_text.empty()
                
                if all_results:
                    st.success(f'✅ Successfully processed {len(df) - len(errors)}/{len(df)} users!')
                    
                    results_df = pd.DataFrame(all_results)
                    
                    st.subheader('📊 Results Table')
                    st.dataframe(results_df, use_container_width=True, height=400)
                    
                    csv_output = results_df.to_csv(index=False)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Excel export
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
                        st.download_button(
                            '📥 Download Results (CSV)',
                            csv_output,
                            'outputs/multi_user_plan.csv',
                            'text/csv',
                            use_container_width=True
                        )
                    
                    st.markdown("---")
                    st.download_button(
                        '📥 Download Results (JSON)',
                        json.dumps(all_results, indent=2),
                        'multi_user_meal_plans.json',
                        'application/json',
                        use_container_width=True
                    )
                    
                    st.subheader('📈 Summary Statistics')
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric('Total Users', len(df))
                    with col2:
                        st.metric('Successful', len(df) - len(errors))
                    with col3:
                        avg_dev = results_df['Calorie_Deviation_%'].mean()
                        st.metric('Avg Deviation %', f"{avg_dev:.1f}%")
                    with col4:
                        avg_div = results_df['Diversity_Score'].mean()
                        st.metric('Avg Diversity', f"{avg_div:.2f}")
                
                if errors:
                    st.error(f'❌ {len(errors)} errors encountered:')
                    errors_df = pd.DataFrame(errors)
                    st.dataframe(errors_df, use_container_width=True)
        
        except Exception as e:
            st.error(f'Error reading CSV file: {str(e)}')
            st.info('Please check the CSV format matches the requirements in the "CSV Format Guide" tab.')
