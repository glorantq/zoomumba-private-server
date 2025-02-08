def handle_swfOptSet(request, user_id, obj, json_data, config_data):
    json_data["swfOpt"]["sb"] = request["sb"]
    json_data["swfOpt"]["se"] = request["se"]
    json_data["swfOpt"]["a"] = request["a"]
    json_data["swfOpt"]["v"] = request["v"]
    json_data["swfOpt"]["w"] = request["w"]
    json_data["swfOpt"]["t"] = request["t"]
    json_data["swfOpt"]["q"] = request["q"]

    # Send to game
    obj["swfOpt"] = json_data["swfOpt"]