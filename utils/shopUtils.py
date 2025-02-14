def is_item_unlocked(config_data_for_item, user_level):
    if config_data_for_item["buyable"] != 1:
        return -1
    if config_data_for_item["onlyDev"] == 1:
        return -1
    if user_level >= config_data_for_item["userLevelRequired"] and config_data_for_item["buyVirtual"] != 0:
        return 1
    if config_data_for_item["buyReal"] != 0:
        return 0
    return -1

def buy_from_shop(config_data_for_item, user_level, json_data):
    is_unlocked = is_item_unlocked(config_data_for_item, user_level)
    if is_unlocked == 1:
        # Buy with virtual currency
        json_data["uObj"]["uCv"] -= config_data_for_item["buyVirtual"]
    elif is_unlocked == 0:
        # Buy with real currency
        json_data["uObj"]["uCr"] -= config_data_for_item["buyReal"]

def buy_multiple_from_shop(config_data_for_item, user_level, json_data, amount):
    is_unlocked = is_item_unlocked(config_data_for_item, user_level)
    if is_unlocked == 1:
        # Buy with virtual currency
        json_data["uObj"]["uCv"] -= amount * config_data_for_item["buyVirtual"]
    elif is_unlocked == 0:
        # Buy with real currency
        json_data["uObj"]["uCr"] -= amount * config_data_for_item["buyReal"]