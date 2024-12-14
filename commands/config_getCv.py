from pathlib import Path
import os
import json

def handle_getCv(request, user_id, obj, json_data, config_data):
    p = Path(__file__).parents[1]
    f = open(os.path.join(p, "data", "getCv.json.def"), "r")
    cv = json.loads(str(f.read()))

    obj["cv"] = cv