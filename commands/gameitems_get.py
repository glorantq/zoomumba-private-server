
def handle_gameitemsGet(request, user_id, obj, json_data, config_data):
    obj["gameItems"] = config_data["gameItems"]