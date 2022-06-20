from flask import  redirect, render_template, request, url_for
# utils is a file in which there is a save_file function for saving images
from application.utils import save_file
from flask_classful import FlaskView, route
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from application import login_manager
# In models directory there is a models file from which all the models are imported
# application acts as main module for this project
from application.models.models import *

# Home Class same as Blueprint
# @login_required mean cannot a person cannot access the home page without login
class HomeView(FlaskView):
    @route('/home')
    @login_required
    def home(self):
        # fetching all the plants from plants model/table
        all_plants = Plants.query.all()
        # Rendering the index page and sending it all the the data that we have fetched
        return render_template('index.html', all_plants=all_plants)

    # add new plant route allows GET and POST requests
    @route('/add_new_plant', methods=['GET', 'POST'])
    def add_new_plant(self):
        # if request method is post which is in the html form and current user
        # is registered then then will access the current the current_user
        # and will access all the values of the form as well
        if request.method == 'POST':
            if current_user.is_authenticated:
                curr_user = current_user
                # the values that we have gotten from html form
                plant_name = request.form.get('plant_name')
                line_one = request.form.get('line_one')
                line_two = request.form.get('line_two')
                line_three = request.form.get('line_three')
                line_four = request.form.get('line_four')
                line_five = request.form.get('line_five')
                plant_image = request.files['plant_image']
                #save_file function will save the image and in images folder
                # and will get the name of the image save_file function is defined in utils file
                isSaved, file_name = save_file(plant_image,'images')
                # new plant is the instance of the Plant class defined in models in which we will 
                #pass all the values and those values will be saved in the plant table of database
                new_plant = Plants(plant_name=plant_name, line_one=line_one, 
                line_two=line_two, line_three=line_three, line_four=line_four, line_five=line_five,
                plant_image=file_name, user_id=curr_user.id)
                # new_plant instace will be added to the database
                # we have imported db from __init__ file
                db.session.add(new_plant)
                # Then we will do commit to the database
                db.session.commit()
                # after successful insertion user will be redirected to home router(home page) in HomeView class
                return redirect(url_for('HomeView:home'))
        else:
            # if request is GET not POST then addPlant.html page will be rendered
            return render_template('addPlant.html')

    
    # in update_plant route we will update the plant here we have fetched the id of
    # the plant which has to be updated please see line number 20 in index.html. This will
    # happen after clicking on a card
    @route('/update_plant/<int:id>', methods=['GET', 'POST'])
    def update_plant(self, id):
        # Through this query we will get the specific plant through its id
        plant = Plants.query.get_or_404(id)
        # if request method is post which is in the html form 
        #  the we will access all the values of the form
        if request.method == "POST":
            plant_name = request.form.get('plant_name')
            line_one = request.form.get('line_one')
            line_two = request.form.get('line_two')
            line_three = request.form.get('line_three')
            line_four = request.form.get('line_four')
            line_five = request.form.get('line_five')
            plant_image = request.files['plant_image']
            isSaved, file_name = save_file(plant_image,'images')
            # Now the plant info that we have gotten in the above query
            # we will access all the info and will assign the new info instead
            plant.plant_name = plant_name
            plant.line_one = line_one
            plant.line_two = line_two
            plant.line_three = line_three
            plant.line_four = line_four
            plant.line_five = line_five
            plant.plant_image = file_name
            db.session.commit()
            return redirect(url_for('HomeView:home'))
        else:
            return render_template('updatePlant.html', plant=plant)
