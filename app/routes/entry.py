# These routes are an example of how to use data, forms and routes to create
# a forum where a posts and comments on those posts can be
# Created, Read, Updated or Deleted (CRUD)

from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Entry
from app.classes.forms import EntryForm
from flask_login import login_required
import datetime as dt

@app.route('/entry/list')
# This means the user must be logged in to see this page
@login_required
def entryList():
    entrys = Entry.objects()
    return render_template('entryposts.html',entrys=entrys)

@app.route('/entry/<entryID>')
# This route will only run if the user is logged in.
@login_required
def entry(entryID):
    # retrieve the post using the postID
    thisEntry = Entry.objects.get(id=entryID)
    return render_template('entrypost.html',entry=thisEntry)

@app.route('/entry/delete/<entryID>')
# Only run this route if the user is logged in.
@login_required
def entryDelete(entryID):
    deleteEntry = Entry.objects.get(id=entryID)
    if current_user == deleteEntry.author:
        deleteEntry.delete()
        flash('The Entry was deleted.')
    else:
        flash("You can't delete an entry you don't own.")
    entrys = Entry.objects()  
    return render_template('entryposts.html',entrys=entrys)

@app.route('/entry/new', methods=['GET', 'POST'])
@login_required
def entryNew():
    entryform = EntryForm()

    if entryform.validate_on_submit():
        newEntry = Entry(
            entrycontent = entryform.entrycontent.data,
            modifydate = dt.datetime.utcnow 
        )
        newEntry.save()

        return redirect(url_for('entry',entryID=newEntry.id))
    
    return render_template('entryform.html',entryform=entryform)

@app.route('/entry/edit/<entryID>', methods=['GET', 'POST'])
@login_required
def entryEdit(entryID):
    editEntry = Entry.objects.get(id=entryID)
    if current_user != editEntry.author:
        flash("You can't edit an entry you don't own.")
        return redirect(url_for('entry',entryID=entryID))
    entryform = EntryForm()
    if entryform.validate_on_submit():
        editEntry.update(
            entrycontent = entryform.entrycontent.data,
            modifydate = dt.datetime.utcnow 
        )
        return redirect(url_for('entry',entryID=entryID))

    entryform.entrycontent.data = editEntry.entrycontent

    return render_template('entryform.html',entryform=entryform)