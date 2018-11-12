from lx_blog import create_app,db,models
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
'''
manange.py is a script to start the app and manange the 
project info of all class
so,in this file only the process od startup is stored,
not how the app create,how to create the db,etc
'''
#create object of flask
app=create_app("develop")
manager=Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)


if __name__ == '__main__':
    manager.run()
