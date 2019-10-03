#########################
# __init__ blueprint
#########################

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from flask_cors import CORS

import json, logging, os, config

app = Flask(__name__)

# to prevent error options 500
CORS(app)

try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

except Exception as e:
    raise e

###################
# Set Database
###################

app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

########
# JWT
########

app.config['JWT_SECRET_KEY'] = '6_SY)9<$F8L[rSK-S'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

##############
# Middlewares
##############

@app.after_request 
def after_request(response):
    try:
        if request.method == 'GET':  
            app.logger.warning("REQUEST_LOG\t%s", 
                json.dumps({
                    'method':request.method,
                    'code':response.status,
                    'uri':request.full_path,
                    'request':request.args.to_dict(), 
                    'response':json.loads(response.data.decode('utf-8'))
                    })
            )
        else:
            app.logger.warning("REQUEST_LOG\t%s", 
                json.dumps({
                    'uri':request.full_path,
                    'request':request.get_json(), 
                    'response':json.loads(response.data.decode('utf-8'))
                    })
            )
    except Exception as e:
        app.logger.error("REQUEST_LOG\t%s",
            json.dumps({
                'uri':request.full_path,
                'request':{}, 
                'response':json.loads(response.data.decode('utf-8'))
                })
        )
    return response

########################
# Import blueprints
#######################

# from blueprints.user.resources import bp_user
# from blueprints.product.resources import bp_product
# from blueprints.auth import bp_auth
# from blueprints.user_detail.resources import bp_user_details
# from blueprints.transaction.resources import bp_transaction
# from blueprints.cart.resources import bp_cart
# from blueprints.product_detail.resources import bp_product_detail
# from blueprints.transaction_detail.resources import bp_trans_details

# app.register_blueprint(bp_user, url_prefix = '/register')
# app.register_blueprint(bp_product, url_prefix = '/product')
# app.register_blueprint(bp_auth, url_prefix = '/login')
# app.register_blueprint(bp_user_details, url_prefix = '/user_details')
# app.register_blueprint(bp_transaction, url_prefix = '/transaction')
# app.register_blueprint(bp_cart, url_prefix = '/cart')
# app.register_blueprint(bp_product_detail, url_prefix = '/product_details')
# app.register_blueprint(bp_trans_details, url_prefix = '/transaction_details')

# db.create_all()
