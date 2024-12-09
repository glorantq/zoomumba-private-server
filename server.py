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
        "swfCookie.set": handle_swfCookieSet
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
        return render_template("play.html")
    
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
        total_response["obj"] = {}

        if "sid" in request.form:
            total_response["obj"]["zoo_sid"] = request.form["sid"]
        else:
            total_response["obj"]["zoo_sid"] = "test"

        f = open(os.path.join(p, "data", "8299495.json"), "r")
        json_data = json.loads(str(f.read()))

        f = open(os.path.join(p, "data", "global_config_data.json.def"), "r")
        config_data = json.loads(str(f.read()))

        callstack = json.loads(request.form["json"])["callstack"]
        for i in callstack:
            command = list(i.keys())[0]

            if command in available_commands:
                print("Command " + command + " handled")
                handler = available_commands[command]
                total_response["obj"] = handler(command, request.args["uId"], total_response["obj"], json_data, config_data)
                total_response["callstack"][0].append({"t":1,"v":""})
            else:
                print("Command " + command + " not handled")

        #print(total_response)  
        return total_response
    
    
    ########
    # MAIN #
    ########
    
    print(" [+] Running server...")

    app.secret_key = 'SECRET_KEY'
    app.run(host=host, port=port, debug=True)

if __name__ == '__main__':
    main()
