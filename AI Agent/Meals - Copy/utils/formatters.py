import json


def plan_to_csv(plan: dict) -> str:
    rows = []
    for meal, v in plan.items():
        rows.append({'meal': meal, 'items': ';'.join(v['items']), 'calories': v['calories']})
    header = 'meal,items,calories\n'
    lines = [f"{r['meal']},\"{r['items']}\",{r['calories']}" for r in rows]
    return header + '\n'.join(lines)


def save_json(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)

