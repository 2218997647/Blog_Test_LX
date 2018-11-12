#define bule
from flask import Blueprint
#create object of bule
api=Blueprint("api_v1",__name__)
#import the view func of the blueprint,so when import in
#in lx_blog/__init__,it can find the demo(when regist
#ter or import api,it will only run __init__ )
from . import demo,passport,article,profile