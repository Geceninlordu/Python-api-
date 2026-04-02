from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Not(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    icerik = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "baslik": self.baslik,
            "icerik": self.icerik
        }
