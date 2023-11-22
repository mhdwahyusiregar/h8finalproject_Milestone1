from datetime import datetime
from config import db, ma

class Development(db.Model):
    __tablename__ = 'development'
    development_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    city = db.Column(db.String(32))
    description = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DevelopmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Development
        sqla_session = db.session    
