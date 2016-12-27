import os
from flask.ext.script import Manager
from capstone import app
from capstone.database import session, User, Profile_Analysis

#create instance of Manager object
manager = Manager(app)

#start development server
@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    

def adduser():
    user = User(
        url= "",
        city=city,
        price = price,
        rating = rating,
        review = review,
        response_time = response_time
        )
        session.save(user)

if __name__ == "__main__":
    manager.run()