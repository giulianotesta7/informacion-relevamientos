#AUTENTICACION DE USUARIOS

from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__) 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form.get('mail')
        password = request.form.get('password')

        user = User.query.filter_by(mail=mail).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Ingreso exitoso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Contraseña incorrecta', category='error')
        else:
            flash('El usuario no existe', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return (redirect(url_for('auth.login')))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        mail = request.form.get('mail')
        fullName = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if User.query.filter_by(mail=mail).first():
            flash('El correo ya existe', category='error')
        elif len(mail) < 4:
            flash('El correo tiene que tener mas de 4 caracteres', category='error')
        elif len(fullName) < 2:
            flash('El nombre tiene que tener mas de 2 caracteres', category='error')
        elif len(password1) <= 7:
            flash('La contraseña tiene que tener al menos 7 caracteres', category='error')
        elif password1 != password2:
            flash('Las contraseñas no coinciden', category='error')
        else:
            new_user = User(mail=mail, fullName=fullName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Cuenta registrada!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)