from app import db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    company = db.Column(db.String(240))
    release = db.Column(db.String(240))
    email = db.Column(db.String(240))

    def __repr__(self):
        return self.name
