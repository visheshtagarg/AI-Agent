# 📋 CSV Format Guide for Batch Meal Planning

This guide explains the required format for uploading CSV files to generate meal plans for multiple users.

## Required Columns

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| **UserID** | string | Unique user identifier | "user_001" |
| **Name** | string | User's name | "Aarav" |
| **Age** | int | Age (10-100) | 25 |
| **Gender** | string | Male / Female / Other | "Male" |
| **Goal** | string | See goals below | "Muscle gain" |
| **Diet_Preference** | string | Vegetarian / Non-vegetarian / Vegan / Pescatarian | "Non-vegetarian" |
| **Meals_Per_Day** | int | Number of meals (1-6) | 5 |

## Optional Columns

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| **Target_Calories** | int | Daily calorie target (800-4500). If missing, auto-calculated | 2800 |
| **Allergies** | string | Comma-separated allergies | "Peanuts, Dairy" |
| **Health_Conditions** | string | Comma-separated conditions | "Low sugar, Diabetes" |
| **Activity_Level** | string | Low / Medium / High (optional) | "Medium" |
| **Cuisine_Preference** | string | Indian / Continental / Mixed / Any (optional) | "Indian" |
| **Meal_Times** | string | Semicolon-separated meal times (HH:MM format). Must match Meals_Per_Day count. If missing, defaults used | "07:30;12:30;16:00;19:30;21:00" |

## Available Goals

- Weight loss
- Weight maintenance
- Muscle gain
- Fat loss
- Balanced diet
- Keto
- Low-carb
- High-protein
- Diabetic-friendly
- Heart-healthy
- Pescatarian
- Gluten-free

## Available Diet Preferences

- Vegetarian
- Non-vegetarian
- Vegan
- Pescatarian

## Meal Count

- **Minimum:** 1 meal per day
- **Maximum:** 6 meals per day
- Values outside this range will be automatically clipped

## Example CSV

```csv
UserID,Name,Age,Gender,Goal,Target_Calories,Diet_Preference,Meals_Per_Day,Allergies,Health_Conditions,Meal_Times,Activity_Level,Cuisine_Preference
U001,Aarav,25,Male,Muscle gain,2800,Non-vegetarian,5,None,None,07:00;11:30;15:30;19:00;21:30,High,Indian
U002,Visheshta,22,Female,Weight loss,1800,Vegetarian,3,None,Low sugar,08:00;13:00;19:00,Medium,Continental
U003,Priya,30,Female,Balanced diet,2000,Vegan,3,Peanuts,None,08:00;13:00;19:30,Low,Indian
```

## Output CSV Format

The generated output CSV will contain:

| Column | Description |
|--------|-------------|
| UserID | Unique user identifier |
| Name | User's name |
| Goal | Selected goal |
| Meals_Per_Day | Number of meals |
| Meal | Name of the meal (Breakfast, Lunch, etc.) |
| Meal_Time | Time for this meal (HH:MM format) |
| Items | Meal items (semicolon-separated) |
| Meal_Calories | Calories for this meal |
| Total_Calories | Total calories for the day |
| Target_Calories | Target calorie goal |
| Calorie_Deviation_% | Deviation from target |

## Notes

- Column names are case-insensitive
- Missing optional columns will use defaults
- Invalid `Meals_Per_Day` values will be clipped to 1-6 range
- If `Target_Calories` is missing, it will be estimated based on age, gender, and goal

