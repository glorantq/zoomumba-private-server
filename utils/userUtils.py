def get_total_user_count():
    return total_user_count

def set_total_user_count(count):
    global total_user_count
    total_user_count = count

def get_zoo_from_db_by_userid(data_db, userid):
    return data_db.find_one({'id': userid})