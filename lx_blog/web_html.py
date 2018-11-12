from flask import Blueprint,current_app,make_response
from flask_wtf import csrf
#our static resounces are stored in the file static/html,so when we vist the index.html
#the url may be 127.0.0.1:5000/();127.0.0.1:5000/static/html/(index.html),it is unfriendly,
# the friendly style is like this
#127.0.0.1:5000/();127.0.0.1:5000/(index.html);
# so,we create the blueprint

#privide the blueprint of static file
html=Blueprint("web_html",__name__)

@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    if not html_file_name:
        html_file_name="index.html"
    html_file_name="html/"+html_file_name

    #create a csrf_token
    csrf_token=csrf.generate_csrf()


    resp=make_response(current_app.send_static_file(html_file_name))
    #set cookies
    resp.set_cookie("csrf_token", csrf_token)
        #a func to return static file
    return resp


