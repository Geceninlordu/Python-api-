from flask import Flask, jsonify, request
from models import db, Not


app = Flask(__name__)

from flask import render_template

# Anasayfa route’u
@app.route('/')
def index():
    return render_template('index.html')

# Veritabanı ayarı (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notlar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Veritabanını oluştur
with app.app_context():
    db.create_all()

# Tüm notları listeleme
@app.route('/api/notlar', methods=['GET'])
def get_notlar():
    notlar = Not.query.all()
    return jsonify([n.to_dict() for n in notlar])

# Yeni not ekleme
@app.route('/api/notlar', methods=['POST'])
def add_not():
    data = request.get_json()
    if not data or not data.get('baslik') or not data.get('icerik'):
        return jsonify({"error": "Baslik ve icerik zorunludur"}), 400
    
    yeni_not = Not(baslik=data['baslik'], icerik=data['icerik'])
    db.session.add(yeni_not)
    db.session.commit()
    return jsonify(yeni_not.to_dict()), 201

# Not silme
@app.route('/api/notlar/<int:not_id>', methods=['DELETE'])
def delete_not(not_id):
    not_obj = Not.query.get(not_id)
    if not not_obj:
        return jsonify({"error": "Not bulunamadı"}), 404
    db.session.delete(not_obj)
    db.session.commit()
    return jsonify({"message": "Not silindi"})

# Not güncelleme
@app.route('/api/notlar/<int:not_id>', methods=['PUT'])
def update_not(not_id):
    not_obj = Not.query.get(not_id)
    if not not_obj:
        return jsonify({"error": "Not bulunamadı"}), 404
    
    data = request.get_json()
    if data.get('baslik'):
        not_obj.baslik = data['baslik']
    if data.get('icerik'):
        not_obj.icerik = data['icerik']
    
    db.session.commit()
    return jsonify(not_obj.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
