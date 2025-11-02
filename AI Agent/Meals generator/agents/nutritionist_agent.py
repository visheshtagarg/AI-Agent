import random
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class NutritionistAgent:
    def __init__(self, rag_retriever=None, model_path='models/lora_meal_generator'):
        self.rag = rag_retriever
        self.model_path = model_path
        if os.path.exists(model_path):
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            except Exception:
                self.tokenizer = None
                self.model = None
        else:
            self.tokenizer = None
            self.model = None

    def generate_meals(self, profile: dict, calorie_plan: dict) -> dict:
        meals = {}
        for meal, meal_data in calorie_plan.items():
            if isinstance(meal_data, dict):
                kcal = meal_data.get('calories', 0)
                meal_time = meal_data.get('meal_time', '')
            else:
                kcal = meal_data
                meal_time = ''
            items = self._generate_items_for_meal(profile['diet_pref'], kcal)
            nutrition = self._get_nutrition_estimate(items)
            meals[meal] = {'items': items, 'calories': kcal, 'nutrition': nutrition, 'meal_time': meal_time}
        return meals

    def _generate_items_for_meal(self, diet_pref, kcal):
        veg_breakfast = ["Oats with milk and banana", "Poha with peanuts", "Idli with sambar"]
        nonveg_breakfast = ["Egg omelette with toast", "Chicken sandwich"]
        veg_lunch = ["Brown rice with dal and salad", "Chapati with paneer curry and salad"]
        nonveg_lunch = ["Chicken curry with rice and salad"]
        snacks = ["Apple", "Greek yogurt", "Roasted chana"]
        dinner = ["Vegetable soup with roti", "Paneer stir-fry with veggies and roti"]

        if diet_pref.lower().startswith('veg'):
            pool = veg_breakfast + veg_lunch + snacks + dinner
        else:
            pool = nonveg_breakfast + nonveg_lunch + snacks + dinner

        count = 1 if kcal < 300 else 2
        items = random.sample(pool, k=min(count, len(pool)))
        return items

    def _get_nutrition_estimate(self, items):
        facts = {item: {'calories': None, 'protein_g': None, 'carbs_g': None, 'fat_g': None} for item in items}
        if self.rag:
            for item in items:
                try:
                    q = self.rag.query(item, n_results=1)
                    if q and 'ids' in q and len(q['ids']) > 0:
                        facts[item]['calories'] = q['metadatas'][0].get('calories') if q['metadatas'] else None
                except Exception:
                    pass
        return facts

