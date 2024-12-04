if __name__ == '__main__':
      
    #######################
    # Import server stuff #
    #######################
    from bundle import TEMPLATES_DIR, STUB_DIR, STYLES_DIR, ASSETS_DIR
    
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
    
    
    #########################
    # Load global game data #
    #########################
    print(" [+] Loading init data...")
    
    p = Path(__file__).parents[0]
    
    ################################
    # Sort accounts by location id #
    ################################
    
    
    ##########################
    # Load site translations #
    ##########################
    
    ########################################
    # Get total amount of created accounts #
    ########################################
    
    '''
    # GLITCH
    host = '0.0.0.0'
    port = 8080
    server_ip = "http://skyrama.glitch.me"
    assets_ip = "https://cdn.jsdelivr.net/gh/Mima2370/skyrama-private-server/"
    '''
    
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
        callstack = json.loads(request.form["json"])["callstack"]
        for i in callstack:
            print(i.keys())
            if list(i.keys())[0] == "config.getCv":
                return open(os.path.join(p, "getCv.json"), "r")
            if list(i.keys())[0] == "swfCookie.set":
                pass
            if list(i.keys())[0] == "config.getConfig":
                return open(os.path.join(p, "getConfig.json"), "r")
            if list(i.keys())[0] == "init.getUser":
                return open(os.path.join(p, "getUser.json"), "r")
            
        return ""
    
    
    ########
    # MAIN #
    ########
    
    print(" [+] Running server...")

    app.secret_key = 'SECRET_KEY'
    app.run(host=host, port=port, debug=True)

if __name__ == '__main__':
    main()
