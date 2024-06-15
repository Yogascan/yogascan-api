from flask import Flask
from flask_cors import CORS
from flask_restful import Api

# from file_name import function_name
from resources.create_account import CreateAccount
from resources.poses import Poses, Pose
from resources.favorites import getFavorite
from resources.history import History
from resources.prediction import Predict
from resources.login import Login
<<<<<<< HEAD
from resources.update_pic import UpdateProfPic
=======
from resources.delete_account import DeleteAccount
from resources.user import getUser

>>>>>>> 9f9c34d6ec7604bc574c2f52359ca13d708c68f0


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
api.add_resource(getFavorite, '/favorite')

# History
api.add_resource(History, '/history')

# Predict
api.add_resource(Predict, '/prediction')

<<<<<<< HEAD
# Update Profile Picture
api.add_resource(UpdateProfPic, '/updatePict')

=======
# Delete Account
api.add_resource(DeleteAccount, '/delete-account')

# Get User
# Delete Account
api.add_resource(getUser, '/user')
>>>>>>> 9f9c34d6ec7604bc574c2f52359ca13d708c68f0

# Main driver function
if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=True)
