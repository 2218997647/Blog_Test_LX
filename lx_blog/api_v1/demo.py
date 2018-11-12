from . import api
import logging
from flask import current_app
from lx_blog import db,models
############################
#File Name:
#Author:xin.liu
#Created Time: 2018-11-04 19:14:50
############################

@api.route("/index")
def index():
    current_app.logger.error("error info")
    current_app.logger.warn("warn info")
    current_app.logger.info("info info")
    current_app.logger.debug("debug info")
    return "index page"