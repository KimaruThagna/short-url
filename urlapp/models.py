from . import db
from datetime import datetime

class UrlRecord(db.Model):
    __tablename__ = "urlrecord"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024), unique=True, nullable=False)
    shortcode = db.Column(db.String(6), unique=True, nullable=False)
    access_count = db.Column(db.Integer,default=0)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, default=db.func.now(), onupdate=datetime.utcnow()
    )

    def update_access_count(self):
        self.access_count += 1
        db.session.commit()
        
    def to_dict(self): 
        return {"id": self.id,
                "url":self.url,
                "shortcode":self.shortcode,
                "count":self.access_count,
                "created_on":self.created_on,
                "updated_on":self.updated_on}