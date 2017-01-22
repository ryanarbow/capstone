import os
from flask.ext.script import Manager
from capstone import app
from capstone.database import Base
from flask.ext.migrate import Migrate, MigrateCommand


#create instance of Manager object
manager = Manager(app)

#start development server
@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

#migration management
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()