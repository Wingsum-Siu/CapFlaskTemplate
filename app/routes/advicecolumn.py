
from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Advice
from app.classes.forms import AdviceForm
from flask_login import login_required
import datetime as dt

@app.route('/advice/list')
@login_required
def adviceList():
    advices = Advice.objects()
    return render_template('advices.html',advices=advices)


@app.route('/advice/<adviceID>')
@login_required
def advice(adviceID):
    # retrieve the post using the postID
    thisAdvice = Advice.objects.get(id=adviceID)
    return render_template('advice.html',advice=thisAdvice)

@app.route('/advice/delete/<adviceID>')
# Only run this route if the user is logged in.
@login_required
def adviceDelete(adviceID):
    # retrieve the post to be deleted using the postID
    deleteAdvice = Advice.objects.get(id=adviceID)
    # check to see if the user that is making this request is the author of the post.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteAdvice.author:
        # delete the post using the delete() method from Mongoengine
        deleteAdvice.delete()
        # send a message to the user that the post was deleted.
        flash('The Advice Post was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a post you don't own.")
    # Retrieve all of the remaining posts so that they can be listed.
    advices = Advice.objects()  
    # Send the user to the list of remaining posts.
    return render_template('advices.html',advices=advices)

# This route actually does two things depending on the state of the if statement 
# 'if form.validate_on_submit()'. When the route is first called, the form has not 
# been submitted yet so the if statement is False and the route renders the form.
# If the user has filled out and succesfully submited the form then the if statement
# is True and this route creates the new post based on what the user put in the form.
# Because this route includes a form that both gets and posts data it needs the 'methods'
# in the route decorator.
@app.route('/advice/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def adviceNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = AdviceForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new post form. 
        # Post() is a mongoengine method for creating a new post. 'newPost' is the variable 
        # that stores the object that is the result of the Post() method.  
        newAdvice = Advice(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            content = form.content.data,
            advicetype = form.advicetype.data,
            # image = form.image.data,
            # im = form.image("image/jpeg"),
            colorbg = form.colorbg.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modifydate = dt.datetime.utcnow 
        )

        # if form.image.data:
        #     form.image.put(form.image.data, content_type = 'image/jpeg')
        #     newAdvice.save()
        # This is a method that saves the data to the mongoDB database.
        newAdvice.save()

        # Once the new post is saved, this sends the user to that post using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a post so we want 
        # to send them to that post. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('advice',adviceID=newAdvice.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at postform.html to 
    # see how that works.
    return render_template('adviceform.html',form=form)


# This route enables a user to edit a post.  This functions very similar to creating a new 
# post except you don't give the user a blank form.  You have to present the user with a form
# that includes all the values of the original post. Read and understand the new post route 
# before this one. 
@app.route('/advice/edit/<adviceID>', methods=['GET', 'POST'])
@login_required
def adviceEdit(adviceID):
    editAdvice = Advice.objects.get(id=adviceID)
    # if the user that requested to edit this post is not the author then deny them and
    # send them back to the post. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editAdvice.author:
        flash("You can't edit an advice post you don't own.")
        return redirect(url_for('advice',adviceID=adviceID))
    # get the form object
    form = AdviceForm()
    # If the user has submitted the form then update the post.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editAdvice.update(
            content = form.content.data,
            advicetype = form.advicetype.data,
            image = form.image.data,
            colorbg= form.colorbg.data,
            modifydate = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated post using a redirect.
        return redirect(url_for('advice',adviceID=adviceID))

    form.content.data = editAdvice.content
    form.advicetype.data = editAdvice.advicetype
    form.image.data = editAdvice.image
    form.colorbg.data= editAdvice.advicetype
    return render_template('adviceform.html',form=form)
