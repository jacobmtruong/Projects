from flask_app import app
from flask_app.controllers import create
from flask_app.controllers import main
from flask_app.controllers import reg_renew
from flask_app.controllers import transfer
from flask_app.controllers import location





if __name__ == "__main__":
    app.run(debug = True)