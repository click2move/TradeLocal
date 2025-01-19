from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
from .models import Note  # Modell für Notizen
from . import db
import json

views = Blueprint('views', __name__)

# Home-Route: Produktübersicht
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        note = request.form.get('note')  # Für Notizen (falls weiterhin benötigt)

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Note speichern
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

# Warenkorb-Route
@views.route('/warenkorb')
def cart():
    return render_template('Warenkorb.html', user=current_user)

# Aktiv-Route
@views.route('/aktiv')
def aktiv():
    return render_template('aktiv.html', user=current_user)

# Kontakt-Route
@views.route('/kontakt')
def kontakt():
    return render_template('kontakt2.html', user=current_user)

# Route für das Löschen von Notizen (falls benötigt)
@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)  # JSON-Daten verarbeiten
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/produkt/<int:produkt_id>')
def produkt_detail(produkt_id):
    produkt = Product.query.get_or_404(produkt_id)
    return render_template('produkt_detail.html', produkt=produkt)