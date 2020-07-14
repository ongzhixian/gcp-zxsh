################################################################################
# Modules and functions import statements
################################################################################

import logging

from datetime import datetime, timedelta

from helpers.app_runtime import app, app_settings
from helpers.app_helper import view, get_model, require_authentication

from modules.security import aes_encrypt_as_hex

from flask import request, make_response, redirect

################################################################################
# Routes for user management
################################################################################

@app.route('/list/user')
def list_user_get():
    logging.info("In list_user_get()")
    view_model = get_model()
    return view(view_model)


@app.route('/add/user')
def add_user_get():
    logging.info("In list_user_get()")
    view_model = get_model()
    return view(view_model)



# @app.route('/about')
# @require_authentication
# def webroot_about_get():
#     logging.info("In webroot_about_get()")
#     view_model = get_model()
#     return view(view_model)