from werkzeug.security import safe_str_cmp
from resources.user import UserModel



def authenticate(username,password):
    user = UserModel.find_by_username(username)
    # in this case, we are using the Model, not the Resource
    if user and safe_str_cmp(user.password, password):
        # to avoid problems in different characters sets or python version
        return user

def identity(payload):
    # payload is the content of JWT token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id) # instructor sugestion
    # mine
    #if user = User.find_by_id(user_id):
    #    return user
    #else:
    #    return None
