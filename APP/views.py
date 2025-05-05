#RUTAS A DONDE EL USUARIO PUEDE IR Y QUE VISTAS SE VAN A MOSTRAR

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort,jsonify, current_app
from flask_login import login_required, current_user
from .models import User, Relevamientos, Base
from . import db
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

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

@views.route('/ver_visitas', methods=['POST', 'GET'])
@login_required
def ver_visita():
    return render_template('ver_visitas.html', user=current_user)

@views.route('/cargar_visitas', methods=['POST', 'GET'])
@login_required
def cargar_visita():
    if request.method == 'POST':
        title = request.form.get('title')
        base_id = request.form.get('base_id')
        tecnico_id = request.form.get('tecnico_id')
        date = request.form.get('date')

        try:
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
        except ValueError:
            flash("Fecha inválida", category="error")
            return redirect(url_for('views.cargar_visita'))

        base = Base.query.get(base_id)
        tecnico = User.query.get(tecnico_id)

        nuevo_evento = {
        "eventTitle": title,
        "eventStartDate": formatted_date,
        "eventEndDate": formatted_date,
        "eventStartTime": "09:00 AM",
        "eventEndTime": "06:00 PM",
        "eventLocation": base.base if base else "Base desconocida",
        "eventTechnician": tecnico.fullName if tecnico else "Sin técnico asignado",
        "eventUrl": ""
        }


        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(BASE_DIR, 'static', 'data')
        os.makedirs(json_dir, exist_ok=True)

        json_path = os.path.join(json_dir, 'events.json')

        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"events": []}

        data["events"].append(nuevo_evento)

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)

        flash("Relevamiento guardado exitosamente", category="success")
        return redirect(url_for('views.cargar_visita'))

    users = User.query.all()
    bases = Base.query.all()
    return render_template('cargar_visitas.html', user=current_user, users=users, bases=bases)