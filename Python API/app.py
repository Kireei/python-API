import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

import models

with app.app_context():
    db.create_all()

# Endpoint pembeli
@app.route('/pembeli', methods=['POST', 'GET'])
def pembeli_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        try:
            pembeli = models.Pembeli(nama=data['nama'], alamat=data.get('alamat'), no_telepon=data.get('no_telepon'))
            db.session.add(pembeli)
            db.session.commit()
            return jsonify(pembeli.to_dict()), 201
        except KeyError as e:
            return jsonify({'error': f'Missing key: {e}'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'GET':
        pembelis = models.Pembeli.query.all()
        return jsonify([pembeli.to_dict() for pembeli in pembelis]), 200

@app.route('/pembeli/<int:id_pembeli>', methods=['GET', 'PUT', 'DELETE'])
def pembeli_detail_endpoint(id_pembeli):
    pembeli = models.Pembeli.query.get_or_404(id_pembeli)

    if request.method == 'GET':
        return jsonify(pembeli.to_dict()), 200
    elif request.method == 'PUT':
        data = request.get_json()
        pembeli.nama = data.get('nama', pembeli.nama)
        pembeli.alamat = data.get('alamat', pembeli.alamat)
        pembeli.no_telepon = data.get('no_telepon', pembeli.no_telepon)
        db.session.commit()
        return jsonify(pembeli.to_dict()), 200
    elif request.method == 'DELETE':
        db.session.delete(pembeli)
        db.session.commit()
        return '', 204

# Endpoint penjual
@app.route('/penjual', methods=['POST', 'GET'])
def penjual_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        try:
            penjual = models.Penjual(nama=data['nama'])
            db.session.add(penjual)
            db.session.commit()
            return jsonify(penjual.to_dict()), 201
        except KeyError as e:
            return jsonify({'error': f'Missing key: {e}'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif request.method == 'GET':
        penjuals = models.Penjual.query.all()
        return jsonify([penjual.to_dict() for penjual in penjuals]), 200

@app.route('/penjual/<int:id_penjual>', methods=['GET', 'PUT', 'DELETE'])
def penjual_detail_endpoint(id_penjual):
    penjual = models.Penjual.query.get_or_404(id_penjual)

    if request.method == 'GET':
        return jsonify(penjual.to_dict()), 200
    elif request.method == 'PUT':
        data = request