import time
from utils import shopUtils

empty_cage = {"id":-1,"uId":0,"fId":0,"cId":1,"sId":0,"level":1,"x":34,"y":84,"r":0,"male":0,"female":0,"child":0,"build":1605824682,"breed":0,"clean":0,"feed":0,"water":0,"cuddle":0,"sick":0,"health":0,"sfeed":0,"eventId":0,"evEnd":0,"drops":{"cu":{"col":0,"eItem":0,"eCol":0},"cl":{"col":{"id":244,"amount":1},"eItem":0,"eCol":0},"wa":{"col":0,"eItem":0,"eCol":0},"fe":{"col":0,"pp":2,"pl":0,"eItem":0,"eCol":0},"sf":{"col":0,"pp":2,"pl":0,"eItem":0},"pf":{"col":0,"pp":2,"pl":0,"eItem":0},"hl":{"pp":2,"pl":0},"sh":{"pp":3,"pl":0},"eb":{"pp":2,"pl":0},"db":{"pp":2,"pl":0}}}
empty_animal = {"id":-1,"uId":0,"aId":0,"sId":0,"cId":0,"fId":0,"fTime":0}

def handle_fieldFia(request, user_id, obj, json_data, config_data):
    current_field_id = json_data["uObj"]["current_field"]

    match request["fia"]:
        case "bC": # BUY_CAGE
            # Create field object if needed
            if str(current_field_id) not in json_data["fObj"]["cages"]:
                json_data["fObj"]["cages"][str(current_field_id)] = {}

            # Initialize new cage
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

            # Buy item
            config_data_for_cage = config_data["gameItems"]["cages"][str(request["cId"])]
            shopUtils.buy_from_shop(config_data_for_cage, json_data["uObj"]["uLvl"], json_data)

            # Send objects to game
            obj["fObj"] = json_data["fObj"]
            obj["req"] = request["req:"] # typo by bigpoint lol
            obj["uObj"] = json_data["uObj"]


        case "bAC": # BUY_ANIMAL_CAGE
            # Create field object if needed
            if str(current_field_id) not in json_data["animals"]:
                json_data["animals"][str(current_field_id)] = {}
            if str(request["id"]) not in json_data["animals"][str(current_field_id)]:
                json_data["animals"][str(current_field_id)][str(request["id"])] = {}

            # Initialize new animal
            new_animal = empty_animal.copy()
            new_animal["id"] = json_data["next_object_id"]
            new_animal["uId"] = user_id
            new_animal["fId"] = current_field_id
            new_animal["cId"] = request["id"]
            new_animal["aId"] = request["aId"]
            new_animal["sId"] = config_data["gameItems"]["animals"][str(request["aId"])]["speciesId"]

            json_data["next_object_id"] += 1

            json_data["animals"][str(current_field_id)][str(request["id"])][str(new_animal["id"])] = new_animal

            # Get cage
            cage = json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]
            cage["sId"] = new_animal["sId"]

            current_time = int(time.time())

            # Get config data for animal + species
            config_data_for_animal = config_data["gameItems"]["animals"][str(request["aId"])]
            config_data_for_species = config_data["gameItems"]["animalsSpecies"][str(new_animal["sId"])]

            # Setup cage
            male = config_data_for_animal["male"]
            child = config_data_for_animal["child"]
            if male == 1:
                cage["male"] += 1
            elif child == 1:
                cage["child"] += 1
            else:
                cage["female"] += 1

            cage["clean"] = current_time + config_data_for_species["cleanTime"]
            cage["feed"] = current_time + config_data_for_species["feedTime"]
            cage["water"] = current_time + config_data_for_species["waterTime"]
            cage["cuddle"] = current_time + config_data_for_species["cuddleTime"]
            cage["sick"] = current_time
            cage["health"] = current_time + config_data_for_species["healthTime"]

            # Buy item
            shopUtils.buy_from_shop(config_data_for_animal, json_data["uObj"]["uLvl"], json_data)

            # Send objects to game
            obj["fObj"] = json_data["fObj"]
            obj["uObj"] = json_data["uObj"]
            obj["animals"] = json_data["animals"]
            obj["req"] = request["req:"] # typo by bigpoint lol

        case ("fAC" | "wAC"): # FEED_ANIMAL_CAGE or WATER_ANIMAL_CAGE
            current_time = int(time.time())
            species_id = json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["sId"]
            config_data_for_species = config_data["gameItems"]["animalsSpecies"][str(species_id)]

            if request["fia"] == "fAC":
                food_id = config_data_for_species["foodId"]
                food_per_animal = config_data_for_species["foodPerAnimal"]
            elif request["fia"] == "wAC":
                food_id = 1
                food_per_animal = config_data_for_species["waterPerAnimal"]

            # To-do: is there a better way to count the animals?
            count_males = json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["male"]
            count_females = json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["female"]
            count_childs = json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["child"]
            count_total = count_males + count_females + count_childs

            total_food_cost = food_per_animal * count_total

            if json_data["res"][str(food_id)]["cnt"] >= total_food_cost:
                if request["fia"] == "fAC":
                    json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["feed"] = current_time + config_data_for_species["feedTime"]
                elif request["fia"] == "wAC":
                    json_data["fObj"]["cages"][str(current_field_id)][str(request["id"])]["water"] = current_time + config_data_for_species["waterTime"]
                json_data["res"][str(food_id)]["cnt"] -= total_food_cost


            obj["fObj"] = json_data["fObj"]
            obj["res"] = json_data["res"]