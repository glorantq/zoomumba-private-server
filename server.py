if __name__ == '__main__':
      
    #######################
    # Import server stuff #
    #######################
    from bundle import TEMPLATES_DIR, STUB_DIR, STYLES_DIR, ASSETS_DIR
    from commands import *
    
    ##########################
    # Import 3rd party stuff #
    ##########################
    print(" [+] Importing libraries...")
    from flask import Flask, render_template, send_from_directory, request, redirect, session, url_for
    import re
    import random
    import uuid
    import time
    import hashlib
    from pathlib import Path
    import json
    import os
    from concurrent.futures import ProcessPoolExecutor

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
    
    ##########
    # ROUTES #
    ##########
    
    @app.route('/')
    def homepage():
        locale = request.args.get('locale')
        if not locale:
            locale = "en"
        return render_template("home.html", ASSETSIP=assets_ip, LOCALE=locale)
    
    @app.route('/game')
    def gamepage():
        f = open(os.path.join(p, "data", "8299495.json"), "r")
        json_data = json.loads(str(f.read()))
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
