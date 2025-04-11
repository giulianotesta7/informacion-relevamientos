#RUTAS A DONDE EL USUARIO PUEDE IR Y QUE VISTAS SE VAN A MOSTRAR

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort,jsonify, current_app
from flask_login import login_required, current_user
from .models import User, Relevamientos, Base
from . import db
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__) 



@views.route('/')
@login_required
def home():
    bases = Base.query.all()
    print(bases)
    return render_template("home.html", user=current_user, bases=bases) 

@views.route('/base/<base_id>')
@login_required
def base_view(base_id):
        base = Base.query.get(base_id)
        relevamientos = Relevamientos.query.order_by(Relevamientos.date.desc()).all()
        print(relevamientos)
        return render_template(f'/bases_operativas/{base_id}.html', user=current_user, base=base, relevamientos=relevamientos)

@views.route('/base/cargar_relevamiento', methods=['GET', 'POST'])
@login_required
def base_relevamiento():
    if request.method == 'POST': 
        title = request.form.get('title')
        description = request.form.get('description')
        base_id = request.form.get('base_id')

        if len(title) < 1:
            flash('El nombre del informe no puede estar vacio', category='error')
        elif len(description) < 1:
            flash('La descripcion no puede estar vacia', category='error')
        else:
            new_relevamiento = Relevamientos(
                title=title,
                description=description,
                user_id=current_user.id,
                base_id=base_id
            )
            db.session.add(new_relevamiento)
            db.session.commit()
            flash('Relevamiento creado!', category='success')
            return redirect(url_for('views.home'))
    bases = Base.query.all()
    return render_template('/cargar_relevamiento.html', user=current_user, bases=bases)

@views.route('/relevamiento/<int:relevamiento_id>')
@login_required
def ver_relevamiento(relevamiento_id):
    relevamiento = Relevamientos.query.get(relevamiento_id)
    if relevamiento:
        base = Base.query.get(relevamiento.base_id)
        tecnico = User.query.get(relevamiento.user_id)
        return render_template('ver_relevamiento.html', relevamiento=relevamiento, base=base,user=current_user,tecnico=tecnico)
    else:
        abort(404)

