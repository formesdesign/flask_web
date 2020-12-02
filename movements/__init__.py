from flask import Flask

#app = Flask(__name__, instance_relative_config=True)
#app.config.from_object("config") #anem a crear un fichero config
app = Flask(__name__)

from movements import views
