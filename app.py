from flask import Flask
from flask_cors import CORS
from flask_restful import Api

# from file_name import function_name
from resources.create_account import CreateAccount
from resources.poses import Poses, Pose
from resources.favorites import getFavorite, Favorite
from resources.history import History
from resources.history import getHistory
from resources.prediction import Predict
from resources.login import Login
from resources.update_pic import UpdateProfPic
from resources.delete_account import DeleteAccount
from resources.user import getUser



# Flask application
app = Flask(__name__)
CORS(app)
api = Api(app)

# Create Account
api.add_resource(CreateAccount, '/signup')

# Predict
api.add_resource(Login, '/login')

# Pose 
api.add_resource(Poses, '/poses')
api.add_resource(Pose, '/pose/<pose_id>')

# Favorite
api.add_resource(Favorite, '/favorite')
api.add_resource(getFavorite, '/favorites')

# History
api.add_resource(History, '/history')
api.add_resource(getHistory, '/histories')

# Predict
api.add_resource(Predict, '/prediction')

# Update Profile Picture
api.add_resource(UpdateProfPic, '/update-picture')

# Delete Account
api.add_resource(DeleteAccount, '/delete-account')

# Get User
# Delete Account
api.add_resource(getUser, '/user')

# Main driver function
if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=True)
