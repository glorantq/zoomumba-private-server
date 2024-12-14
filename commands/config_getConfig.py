import time
from pathlib import Path
import os
import json

def handle_getConfig(request, user_id, obj, json_data, config_data):
    p = Path(__file__).parents[1]
    f = open(os.path.join(p, "data", "global_config_data.json.def"), "r")
    config = json.loads(str(f.read()))

    obj["config"] = config