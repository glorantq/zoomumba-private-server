if __name__ == '__main__':

    #######################
    # Import server stuff #
    #######################
    from bundle import TEMPLATES_DIR, STUB_DIR, STYLES_DIR, ASSETS_DIR
    from commands import *
    import utils.userUtils as userUtils
    
    ##########################
    # Import 3rd party stuff #
    ##########################
    print(" [+] Importing libraries...")
    from flask import Flask, render_template, send_from_directory, request, redirect, session
    import re
    import secrets
    import time
    import bcrypt
    from pathlib import Path
    import json
    import os
    from pymongo import MongoClient
    from dotenv import load_dotenv

def main():
    print(" [+] Loading server...")
    
    ###############################
    # Setup list of game commands #
    ###############################
    
    available_commands = {
        "config.getCv": handle_getCv,
        "config.getConfig": handle_getConfig,
        "init.getUser": handle_getUser,
        "swfCookie.set": handle_swfCookieSet,
        "tutorial.rS": handle_tutorialRs,
        "field.fia": handle_fieldFia,
        "gameitems.get": handle_gameitemsGet
    }
    
    #########################
    # Load global game data #
    #########################

    print(" [+] Loading init data...")
    
    p = Path(__file__).parents[0]
    
    # LOCAL
    host = '127.0.0.1'
    port = 5050
    server_ip = "http://" + str(host) + ":" + str(port)
    assets_ip = "http://" + str(host) + ":" + str(port)
    
    app = Flask(__name__, template_folder=TEMPLATES_DIR)
    
    print(" [+] Configuring server routes...")

    ######################
    # Connect to MongoDB #
    ######################

    load_dotenv()
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client["zoo-dev"]
    auth_db = db["zoo-auth"]
    data_db = db["zoo-data"]

    userUtils.set_total_user_count(auth_db.estimated_document_count())
    
    ##########
    # ROUTES #
    ##########
    
    @app.route('/')
    def homepage():
        locale = request.args.get('locale')
        if not locale:
            locale = "en"
        session["locale"] = locale
        action = request.args.get('action')
        if "msg" not in session:
            session["msg"] = ""
        msg = session["msg"]
        session["msg"] = ""
        if action == "externalSignUp":
            return render_template("signup.html", ASSETSIP=assets_ip, SERVERIP=server_ip, LOCALE=locale, msg=msg)
        else:
            return render_template("home.html", ASSETSIP=assets_ip, SERVERIP=server_ip, LOCALE=locale, msg=msg, registered=userUtils.get_total_user_count())
    
    @app.route('/authenticate', methods=['POST'])
    def authenticate():
        msg = ''

        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            account_in_db = auth_db.find_one({'username': username})

            if account_in_db and bcrypt.checkpw(password.encode('utf-8'), account_in_db["password"].encode('utf-8')):
                session["username"] = username
                session["userid"] = account_in_db["id"]
                session["token"] = secrets.token_urlsafe(32)
                return redirect("/game")
            else:
                msg = "bgc.error.login_invalidCredentials"
        elif 'username' not in request.form:
            msg = "bgc.error.username_notGiven"
        elif 'password' not in request.form:
            msg = "bgc.error.password_notGiven"

        session["msg"] = msg
        return redirect("/")
    
    @app.route('/register', methods=['POST'])
    def register():
        msg = ''
        if not request.args.get('locale'):
            if "locale" in session:
                locale = session["locale"]
            else:
                locale = "en"
        else:
            locale = request.args.get('locale')
        
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        termsAndConditions = request.form['termsAndConditions']

        # Check requirements
        if username == "":
            msg = "bgc.error.username_notGiven"
        elif password == "":
            msg = "bgc.error.password_notGiven"
        elif email == "":
            msg = "bgc.error.email_notGiven"
        elif len(username) < 4:
            msg = "bgc.error.username_isTooShort"
        elif len(username) > 20:
            msg = "bgc.error.username_isTooLong"
        elif not username.isalnum(): # check for non-alphanumeric characters
            msg = "bgc.error.username_containsInvalidCharacters"
        elif len(password) < 4:
            msg = "bgc.error.password_isTooShort"
        elif len(password) > 45:
            msg = "bgc.error.password_isTooLong"
        elif username == password:
            msg = "bgc.error.password_matchesUsername"
        elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is None:
            msg = "bgc.error.email_invalidAddress"
        elif termsAndConditions == "0":
            msg = "bgc.error.termsAndConditions_notAccepted"
        elif auth_db.find_one({"username": username}):
            msg = "A user with this name already exists"

        if msg != "":
            return render_template("signup.html", ASSETSIP=assets_ip, SERVERIP=server_ip, LOCALE=locale, msg=msg)

        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf8')
    
        highest_id = auth_db.find().sort('id', -1).limit(1) # Find highest id in database (hopefully this doesn't eat performance xd)
        list_highest_id = list(highest_id)
        print(list_highest_id)
        if(len(list(highest_id)) == 0):
            # First user
            id = 1
        else:
            id = list(highest_id)[0]["id"] + 1

        secret_id = secrets.token_urlsafe(32)
        if auth_db.find_one({"sid": secret_id}): # Useless check but you never know xD
            secret_id = secrets.token_urlsafe(32)

        doc_data = {
            "id": id,
            "sid": secret_id,
            "username": username,
            "password": password,
            "email": email,
            "newsletter": "newsletter" in request.form and request.form["newsletter"] == "1", 
        }
        #auth_db.insert_one(doc_data)

        f = open(os.path.join(p, "data", "new_player.json.def"), "r")
        new_player_data = f.read()
        f.close()

        new_player_data = new_player_data.replace("PLACEHOLDER_USERID", str(id))
        new_player_data = new_player_data.replace("PLACEHOLDER_SID", secret_id)
        print(new_player_data[0:300])
        print(fr'{new_player_data[0:300]}')

        # NOTE:
        # We handle field ids different than the original game, instead of a random (probably global) number we do
        # fId = fType (with leading 0 if needed) + userid
        # For example: 018299495 for field type 1 with userid 8299495

        token = secrets.token_urlsafe(32)
        session["token"] = token
        session["username"] = username
        session["userid"] = id

        doc_data = {
            "id": id,
            "sid": secret_id,
            "username": username,
            "token": token,
            "zoo": json.loads(fr'{new_player_data}')
        }
        data_db.insert_one(doc_data)

        userUtils.set_total_user_count(userUtils.get_total_user_count() + 1)

        return redirect("/game")
    
    @app.route("/game")
    def gamepage():
        if "userid" not in session:
            return redirect("/")
        json_data = json.loads(userUtils.get_zoo_from_db_by_userid(data_db, session["userid"])["zoo"])
        tutS = json_data["uObj"]["tutS"]
        tutT = json_data["uObj"]["tutT"]
        return render_template("play.html", tutS=tutS, tutT=tutT)
    
    @app.route("/crossdomain.xml")
    def crossdomain():
        return send_from_directory(STUB_DIR, "crossdomain.xml")
    
    ###############
    # GAME STATIC #
    ###############
    
    @app.route("/assets/<path:path>")
    def static_assets_loader(path):
        return send_from_directory(ASSETS_DIR, path)
    
    
    @app.route("/templates/styles/<path:path>")
    def styles(path):
        return send_from_directory(STYLES_DIR, path)
    
    ################
    # GAME DYNAMIC #
    ################
    
    
    @app.route("/ZooApi.php", methods=['POST'])
    def handle_request():
        print(request.form["json"])

        total_response = {}
        total_response["callstack"] = [[]]
        obj = {}

        if "sid" in request.form:
            obj["zoo_sid"] = request.form["sid"]
        else:
            obj["zoo_sid"] = "test"

        if "sData" not in obj:
            obj["sData"] = {}
        obj["sData"]["time"] = int(time.time())

        f = open(os.path.join(p, "data", "8299495.json"), "r")
        json_data = json.loads(str(f.read()))
        f.close()

        f = open(os.path.join(p, "data", "global_config_data.json.def"), "r")
        config_data = json.loads(str(f.read()))
        f.close()

        callstack = json.loads(request.form["json"])["callstack"]
        for i in callstack:
            command = list(i.keys())[0]
            if command in available_commands:
                print("Command " + command + " handled")
                handler = available_commands[command]
                handler(i[command], request.args["uId"], obj, json_data, config_data)
                total_response["callstack"][0].append({"t":1,"v":""})
            else:
                print("Command " + command + " not handled")

        total_response["obj"] = obj
        f = open(os.path.join(p, "data", "8299495.json"), "w")
        f.write(json.dumps(json_data))
        f.close()
        return total_response
    
    
    ########
    # MAIN #
    ########
    
    print(" [+] Running server...")

    app.secret_key = 'SECRET_KEY'
    app.run(host=host, port=port, debug=True)

if __name__ == '__main__':
    main()
