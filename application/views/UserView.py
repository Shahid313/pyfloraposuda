from flask import  redirect, render_template, request, url_for
from flask_classful import FlaskView, route
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from application import login_manager
from application.models.models import *
from sqlalchemy import text

#login_manager is imported from application (root module)
# which is defined in __init__.py on line number 16 and
# load_user will load a specific user by his/ her id after succesfull login
#It loads user object by user id from session
@login_manager.user_loader 
def load_user(user_id):
	return User.query.get(int(user_id))

class UserView(FlaskView):
    @route('/', methods=['GET', 'POST'])
    def login(self):
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password,password):
                    #The login_user function calls the is_active from UserMixin
                    # and if it is the case then login_user function insert user id into the session
                    login_user(user)
                    return redirect(url_for('HomeView:home'))
                else:
                    return "Your password is incorrect"
            else:
                return "This user does not exist"
        else:
            return render_template('login.html')

    @route('/signup', methods=['GET','POST'])
    def signup(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            # hashed_password function is imported from werkzeug.security package
            hashed_password = generate_password_hash(password,method='sha256')
            new_user = User(username=username, password=hashed_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('UserView:login'))
            except:
                return "There was an issue"
        else:
            return render_template('signup.html')

    # in logout route login is required (@login_required) is imported from
    # flask_login package and when the logout function is called logout_user()
    # function will be called which is imported from flask_login and 
    # user will be redirected to UserView class login route
    @route("/logout")
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('UserView:login'))


    # in profile route login is required (@login_required) is imported from
    # flask_login package
    @route('/profile')
    @login_required
    def profile(self):
        # current_user is imported from flask_login which will give us current user information
        if current_user.is_authenticated:
            curr_user = current_user
            # text is imported from flask sql_alchemy
            profile_sql = text("SELECT * FROM plants WHERE user_id = "+str(curr_user.id))
            profile_plants = db.engine.execute(profile_sql)
            profile_name_sql = text("SELECT * FROM user WHERE id = "+str(curr_user.id))
            profile_name = db.engine.execute(profile_name_sql)
            for user in profile_name:
                name = user.username
            return render_template('profile.html', profile_plants=profile_plants, name=name)


    