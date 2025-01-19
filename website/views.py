from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
from . import db
import json
from .models import Product  # Import der Product-Klasse
views = Blueprint('views', __name__)

# Home-Route: Produktübersicht

@views.route('/', methods=['GET', 'POST'])
def home():
    # Filterlogik (optional)
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    # Produkte aus der Datenbank abfragen
    query = Product.query
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    if category:
        query = query.filter(Product.category == category)

    products = query.all()
    
    return render_template("home.html", products=products)

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


@views.route('/produkt/<int:produkt_id>')
def produkt_detail(produkt_id):
    produkt = Product.query.get_or_404(produkt_id)
    return render_template('produkt_detail.html', produkt=produkt)