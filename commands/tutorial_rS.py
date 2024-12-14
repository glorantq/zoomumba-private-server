
def handle_tutorialRs(request, user_id, obj, json_data, config_data):
    json_data["uObj"]["tutS"] = request["s"]
    json_data["uObj"]["tutT"] = request["t"]