import time

empty_cage = {"id":-1,"uId":0,"fId":0,"cId":1,"sId":0,"level":1,"x":34,"y":84,"r":0,"male":0,"female":0,"child":0,"build":1605824682,"breed":0,"clean":0,"feed":0,"water":0,"cuddle":0,"sick":0,"health":0,"sfeed":0,"eventId":0,"evEnd":0,"drops":{"cu":{"col":0,"eItem":0,"eCol":0},"cl":{"col":{"id":244,"amount":1},"eItem":0,"eCol":0},"wa":{"col":0,"eItem":0,"eCol":0},"fe":{"col":0,"pp":2,"pl":0,"eItem":0,"eCol":0},"sf":{"col":0,"pp":2,"pl":0,"eItem":0},"pf":{"col":0,"pp":2,"pl":0,"eItem":0},"hl":{"pp":2,"pl":0},"sh":{"pp":3,"pl":0},"eb":{"pp":2,"pl":0},"db":{"pp":2,"pl":0}}}
empty_animal = {"id":-1,"uId":0,"aId":0,"sId":0,"cId":0,"fId":0,"fTime":0}

def handle_fieldFia(request, user_id, obj, json_data, config_data):
    current_field_id = json_data["uObj"]["current_field"]

    if str(current_field_id) not in json_data["fObj"]["cages"]:
        json_data["fObj"]["cages"][str(current_field_id)] = {}

    if request["fia"] == "bC": # BUY_CAGE
        new_cage = empty_cage.copy()
        new_cage["id"] = json_data["next_object_id"]
        new_cage["uId"] = user_id
        new_cage["fId"] = current_field_id
        new_cage["cId"] = request["cId"]
        new_cage["x"] = request["x"]
        new_cage["y"] = request["y"]
        new_cage["r"] = request["r"]
        new_cage["build"] = int(time.time()) + 10

        json_data["next_object_id"] += 1
        json_data["fObj"]["cages"][str(current_field_id)][str(new_cage["id"])] = new_cage

        obj["fObj"] = json_data["fObj"]
        obj["req"] = request["req:"] # typo by bigpoint lol

    elif request["fia"] == "bAC": # BUY_ANIMAL_CAGE
        if str(current_field_id) not in json_data["animals"]:
            json_data["animals"][str(current_field_id)] = {}
        if str(request["id"]) not in json_data["animals"][str(current_field_id)]:
            json_data["animals"][str(current_field_id)][str(request["id"])] = {}

        new_animal = empty_animal.copy()
        new_animal["id"] = json_data["next_object_id"]
        new_animal["uId"] = user_id
        new_animal["fId"] = current_field_id
        new_animal["cId"] = request["id"]
        new_animal["aId"] = request["aId"]
        new_animal["sId"] = config_data["gameItems"]["animals"][str(request["aId"])]["speciesId"]

        current_time = int(time.time())

        json_data["next_object_id"] += 1
        json_data["animals"][str(current_field_id)][str(request["id"])][str(new_animal["id"])] = new_animal
        json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["sId"] = new_animal["sId"]

        male = config_data["gameItems"]["animals"][str(request["aId"])]["male"]
        child = config_data["gameItems"]["animals"][str(request["aId"])]["child"]
        if male == 1:
            json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["male"] += 1
        elif child == 1:
            json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["child"] += 1
        else:
            json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["female"] += 1

        json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["clean"] = current_time + config_data["gameItems"]["animalsSpecies"][str(new_animal["sId"])]["cleanTime"]
        json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["feed"] = current_time + config_data["gameItems"]["animalsSpecies"][str(new_animal["sId"])]["feedTime"]
        json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["water"] = current_time + config_data["gameItems"]["animalsSpecies"][str(new_animal["sId"])]["waterTime"]
        json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["cuddle"] = current_time + config_data["gameItems"]["animalsSpecies"][str(new_animal["sId"])]["cuddleTime"]
        json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["sick"] = current_time
        json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["health"] = current_time + config_data["gameItems"]["animalsSpecies"][str(new_animal["sId"])]["healthTime"]

        obj["fObj"] = json_data["fObj"]
        obj["animals"] = json_data["animals"]
        obj["req"] = request["req:"] # typo by bigpoint lol