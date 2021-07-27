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
    urlrecord_id = db.Column(db.Integer, db.ForeignKey("urlrecord.id"))
    urlrecord = db.relationship(
        "UrlRecord", backref=db.backref("urlrecord", uselist=False)
    )
    access_count = db.Column(db.Integer,default=0)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def update_access_count(self):
        self.access_count += 1
        self.save()