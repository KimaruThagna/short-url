from . import db


class UrlRecord(db.Model):
    __tablename__ = "urlrecord"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024), unique=True, nullable=False)
    shortcode = db.Column(db.String(6), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())


class UrlStats(db.Model):
    __tablename__ = "urlstats"
    id = db.Column(db.Integer, primary_key=True)
    shortcode_id = db.Column(db.Integer, db.ForeignKey("urlrecord.id"))
    shortcode = db.relationship(
        "Request", backref=db.backref("urlrecord", uselist=False)
    )
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
