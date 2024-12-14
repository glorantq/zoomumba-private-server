import time

def handle_getUser(request, user_id, obj, json_data, config_data):
    json_data["uObj"]["current_field"] = json_data["fIds"]["1"]
    obj.update(json_data)