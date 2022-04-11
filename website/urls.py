import os
from flask import Blueprint, render_template, flash, request, redirect, session
import json
from werkzeug.utils import secure_filename
from uuid import uuid4
from flask_bcrypt import Bcrypt


from . import DB
from .models import Contacts, Users

views = Blueprint('views', __name__, template_folder='templates',
                  static_url_path='static')


bcrypt = Bcrypt()


@views.route('/', methods=['GET', 'POST'])
@views.route('/singin', methods=['GET', 'POST'])
def home():
    if not (session.get("USER") is None):
        return redirect('/about')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            get_user = Users.query.filter_by(email=email).first()
        except Exception:
            flash("Invalid credentials", 'error')
        else:
            if bcrypt.check_password_hash(get_user.password, password):
                session['USER'] = [get_user.name, get_user.email]

                return redirect('/singup')
    return render_template('index.html')


@views.route('/singup', methods=['GET', 'POST'])
def singup():
    if not (session.get("USER") is None):
        return redirect('/about')

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conform_password = request.form['conform_password']
        profileImg = request.files['profile_img']
        try:
            termsAgree = request.form['termsAgree']
        except Exception:
            flash('Please agree with our terms and conditions', category='error')
        else:
            if password != conform_password and len(password) < 8:
                flash('Do not match passwords', category='error')
            elif len(name) < 2:
                flash("Please enter a valid name", category='error')
            elif len(email) < 7 and "@" not in email:
                flash("Please enter a valid email", category='error')
            else:
                # handle profile photo upload
                fileExtension = secure_filename(profileImg.filename).split('.')
                uniqueFileName = f"{str(uuid4())}.{fileExtension[1]}"
                profileImg.save(os.path.join(
                    "./website/static/images/users", uniqueFileName))

                # hash password
                hashPassword = bcrypt.generate_password_hash(password)
                try:
                    new_user = Users(name=name, email=email,
                                     password=hashPassword, photo=uniqueFileName)
                    DB.session.add(new_user)
                    DB.session.commit()
                except Exception:
                    flash("Invalid credentials", category='error')
                else:
                    flash("Register successfully", category='success')
                    return redirect('/')
    return render_template('singup.html')


@views.route('/logout')
def logout():
    session.pop("USER")
    return redirect("/")


@ views.route('/about')
def about():
    if session.get("USER") is None:
        return redirect("/")
    try:
        get_user = Users.query.filter_by(email=session.get("USER")[1]).first()
    except Exception:
        return redirect('/')
    return render_template('profile.html', user=get_user, profilePhoto=f"images/users/{get_user.photo}")


@ views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        if len(name) < 3:
            flash("Please enter a valid name", category='error')
        elif len(email) < 7 and "@" not in email:
            flash("Please enter a valid email", category='error')
        elif len(subject) < 5:
            flash("Please enter the subject", category='error')
        elif len(message) < 5:
            flask("Please enter the message", category='error')
        else:
            try:
                new_contact = Contacts(
                    name=name, email=email, subject=subject, message=message)
                DB.session.add(new_contact)
                DB.session.commit()
            except Exception:
                flash("Server Error, Pease try again leter", 'error')
            else:
                flash("This is contact  page", category='success')

    return render_template('contact.html')


@views.route('/get_contact_comment', methods=['POST'])
def get_contact_comment():
    try:
        author = request.get_json()
        if author['username'] != os.getenv("USERNAME") and author['password'] != os.getenv("PASSWORD"):
            raise Exception("Invaild credentials")

        response = Contacts.query.filter_by().all()
        response_list = []
        for item in response:
            contact_dict = {"id": item.id, "name": item.name, "email": item.email,
                            "subject": item.subject, "message": item.message, "date": item.date}
            response_list.append(contact_dict)
    except Exception as error:
        return str(error)
    else:
        return {"data": response_list}


@views.route('/delete_contact/<int:id>', methods=['POST'])
def delete_contact(id):
    try:
        response = Contacts.query.get_or_404(id)
        print("hi")
        print(response)
        DB.session.delete(response)
        DB.session.commit()
    except Exception as e:
        return {"error": "DATABSE ERROR"}
    else:
        return {"data": "data has been deleted from database"}
