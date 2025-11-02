import csv
import random


def generate_synthetic_line():
    categories = {
        'Breakfast': ['Oats with milk and banana', 'Idli with sambar', 'Poha with peanuts'],
        'Lunch': ['Brown rice with dal', 'Chapati with paneer curry'],
        'Snack': ['Apple', 'Roasted chana'],
        'Dinner': ['Vegetable soup with roti', 'Paneer stir-fry']
    }
    category = random.choice(list(categories.keys()))
    item = random.choice(categories[category])
    calories = random.randint(100, 800)
    return {'input': f"{calories} kcal {category} {item}", 'target': category}


if __name__ == '__main__':
    with open('data/synthetic_lines.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['input', 'target'])
        w.writeheader()
        for _ in range(2000):
            w.writerow(generate_synthetic_line())

