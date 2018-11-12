from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
from lx_blog.utils.commons import ReConverter
#create db object without bongding app
#when we are creating the db object ,there is no app object
db=SQLAlchemy()

# create redis to store session(in flask,in default,session store in the cookie of fronted)
# create redis connection object
redis_store=None
#factory
def create_app(config_name):
    '''
    create flask object
    :param config_name: str,name of config(Develop or product)
    :return:
    '''
    app = Flask(__name__)
    #get config info according to name of config
    config_class=config_map.get(config_name)
    # load config
    app.config.from_object(config_class)
    #init db via app
    db.init_app(app)

    global redis_store
    redis_store=redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # store data of session to redis via flask_session
    # create session object from session class
    Session(app)

    # add CSRF protect for flask
    #to use this,the cookies and request body(post\put\delete no get) must have value
    CSRFProtect(app)

    # 配置日志信息
    # 设置日志的记录等级
    logging.basicConfig(level=logging.INFO)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日记录器
    logging.getLogger().addHandler(file_log_handler)
    '''
    #set the level of log
    logging.basicConfig(level=logging.DEBUG)
    #create log handler(path,maxBytes for each log file,max number of files to store)
    file_log_handler=RotatingFileHandler("logs/log",maxBytes=1024*1024,backupCount=10)
    #create the format of the log
    formatter=logging.Formatter('%(levelname)$ %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    #add log handler to flask app
    logging.getLogger().addHandler(file_log_handler)'''

    #add self-defined convert to flask
    app.url_map.converters["re"]=ReConverter

    #register blueprint
    from lx_blog import api_v1
    app.register_blueprint(api_v1.api,url_prefix="/api_v1")

    from lx_blog import web_html
    app.register_blueprint(web_html.html)


    return app